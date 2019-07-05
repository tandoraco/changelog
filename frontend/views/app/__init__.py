from urllib.parse import unquote

from django.http import Http404
from django.shortcuts import render
from django.views.generic import ListView

from frontend.custom.decorators import check_auth
from frontend.views.auth.mixins import LoginRequiredMixin
from v1.accounts.models import Company
from v1.core.models import Changelog


def index(request):
    return render(request, 'app.html')


class ChangeLogList(LoginRequiredMixin, ListView):
    paginate_by = 20
    template_name = 'app.html'

    def get_template_names(self):
        if int(self.request.GET.get('page', 1)) > 1:
            return ['changelog_items.html']
        return ['app.html']

    def get_queryset(self):
        return Changelog.objects.filter(deleted=False).order_by('-created_at')


@check_auth
def view_changelog(request, slug):
    try:
        changelog = Changelog.objects.get(slug=unquote(slug))
        return render(request, 'single-changelog.html',
                      context={'title': changelog.title, 'content': changelog.content})
    except Changelog.DoesNotExist:
        raise Http404


def view_changelog_as_public(request, company, changelog_terminology, slug):
    try:
        company = Company.objects.get(company_name__iexact=company, changelog_terminology__iexact=changelog_terminology)
        changelog = Changelog.objects.get(slug=unquote(slug), published=True, deleted=False)
        return render(request, 'public-single-changelog.html',
                      context={'company_name': company.company_name, 'terminology': changelog_terminology,
                               'title': changelog.title, 'content': changelog.content,
                               'color': changelog.category.color})
    except (Company.DoesNotExist, Changelog.DoesNotExist):
        raise Http404


def public_index(request, company, changelog_terminology):
    try:
        company = Company.objects.get(company_name__iexact=company, changelog_terminology__iexact=changelog_terminology)
        changelogs = Changelog.objects.filter(deleted=False, published=True).order_by('-created_at')
        return render(request, 'public-index.html',
                      context={'company_name': company.company_name, 'terminology': changelog_terminology,
                               'changelogs': changelogs})
    except (Company.DoesNotExist, Changelog.DoesNotExist):
        raise Http404
