from django.contrib import messages
from django.http import HttpResponseRedirect, Http404
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
    data = {'request': request}
    return _changelog_form(request, ChangelogForm(initial=data), "create")


@check_auth
def edit_changelog(request, id):
    try:
        company_id = request.session["company-id"]
        changelog = Changelog.objects.get(company__id=company_id, pk=id)
        data = {'published': changelog.published, 'request': request}
        form = ChangelogForm(instance=changelog, initial=data)
        return _changelog_form(request, form, "edit", changelog_id=id, instance=changelog)
    except Changelog.DoesNotExist:
        messages.error(request, message=CHANGELOG_DOES_NOT_EXIST_ERROR)
        raise Http404


def _changelog_form(request, form, action, changelog_id=None, instance=None):
    if request.method == "POST":
        initial = {'request': request}
        form = ChangelogForm(request.POST, initial=initial) if not instance else ChangelogForm(request.POST, instance,
                                                                                               initial=initial)
        data = request.POST.copy()
        data["company"] = request.session["company-id"]
        if not instance:
            data["created_by"] = request.session["user-id"]
        else:
            data["created_by"] = instance.created_by.id

        data["last_edited_by"] = request.session["user-id"]

        serializer = ChangelogSerializer(data=data) if not instance else ChangelogSerializer(instance, data=data)
        if serializer.is_valid():
            serializer.save()
            messages.success(request, message=CHANGELOG_CREATED_OR_EDITED_SUCCESSFULLY.format(f"{action}"))
            return HttpResponseRedirect("/staff/changelogs")

    changelog_id = f"/{str(changelog_id)}" if changelog_id else ""

    return render(request, 'changelog-form.html',
                  {'form': form, 'action': f'/staff/{action}-changelog{changelog_id}', 'title': action.title()})


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
