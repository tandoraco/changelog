from django.http import HttpResponseRedirect
from django.shortcuts import render

from frontend.custom.decorators import check_auth
from frontend.forms.core.changelog import NewChangelogForm
from v1.core.serializers import ChangelogSerializer


@check_auth
def new_changelog(request):
    form = NewChangelogForm()
    if request.method == "POST":
        form = NewChangelogForm(request.POST)
        data = request.POST.copy()
        data["created_by"] = request.session["user-id"]
        data["last_edited_by"] = request.session["user-id"]

        serializer = ChangelogSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponseRedirect("/changelogs")

    return render(request, 'new-changelog.html', {'form': form})
