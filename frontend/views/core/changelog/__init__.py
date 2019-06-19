from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render

from frontend.constants import CHANGELOG_DOES_NOT_EXIST_ERROR, CHANGELOG_CREATED_OR_EDITED_SUCCESSFULLY, \
    CHANGELOG_DELETED_SUCCESSFULLY
from frontend.custom.decorators import check_auth
from frontend.forms.core.changelog import ChangelogForm
from v1.accounts.models import User
from v1.core.models import Changelog
from v1.core.serializers import ChangelogSerializer


@check_auth
def changelog_form(request):
    return _changelog_form(request, ChangelogForm(), "create")


@check_auth
def edit_changelog(request, id):
    try:
        changelog = Changelog.objects.get(pk=id)
        form = ChangelogForm(instance=changelog)
        return _changelog_form(request, form, "edit", changelog_id=id, instance=changelog)
    except Changelog.DoesNotExist:
        messages.error(request, message=CHANGELOG_DOES_NOT_EXIST_ERROR)
        return HttpResponseRedirect("/changelogs")


def _changelog_form(request, form, action, changelog_id=None, instance=None):
    if request.method == "POST":
        form = ChangelogForm(request.POST) if not instance else ChangelogForm(request.POST, instance)
        data = request.POST.copy()
        data["created_by"] = request.session["user-id"]
        data["last_edited_by"] = request.session["user-id"]

        serializer = ChangelogSerializer(data=data) if not instance else ChangelogSerializer(instance, data=data)
        if serializer.is_valid():
            serializer.save()
            messages.success(request, message=CHANGELOG_CREATED_OR_EDITED_SUCCESSFULLY.format(f"{action}"))
            return HttpResponseRedirect("/changelogs")

    changelog_id = f"/{str(changelog_id)}" if changelog_id else ""

    return render(request, 'changelog-form.html',
                  {'form': form, 'action': f'/{action}-changelog{changelog_id}', 'title': action.title()})


@check_auth
def delete_changelog(request, id):
    try:
        changelog = Changelog.objects.get(id=id)
        changelog.deleted = True
        changelog.last_edited_by = User.objects.get(pk=request.session["user-id"])
        changelog.save()

        messages.success(request, message=CHANGELOG_DELETED_SUCCESSFULLY)
    except Changelog.DoesNotExist:
        messages.error(request, message=CHANGELOG_DOES_NOT_EXIST_ERROR)

    return HttpResponseRedirect("/")
