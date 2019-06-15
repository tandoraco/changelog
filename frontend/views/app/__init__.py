from django.http import Http404
from django.shortcuts import render
from django.views.generic import ListView

from v1.core.models import Changelog


def index(request):
    return render(request, 'app.html')


class ChangeLogList(ListView):
    paginate_by = 20
    template_name = 'app.html'

    def get_template_names(self):
        if int(self.request.GET.get('page', 1)) > 1:
            return ['changelog_items.html']
        return ['app.html']

    def get_queryset(self):
        return Changelog.objects.all().order_by('-created_at')


def view_changelog(request, slug):
    try:
        changelog = Changelog.objects.get(slug=slug)
        return render(request, 'single-changelog.html',
                      context={'title': changelog.title, 'content': changelog.content})
    except Changelog.DoesNotExist:
        raise Http404
