from urllib.parse import unquote

from django.db import transaction
from django.http import Http404
from django.shortcuts import render

from frontend.custom.decorators import is_authenticated
from frontend.custom.utils import get_company_from_slug_and_changelog_terminology
from frontend.custom.views import TandoraListViewMixin
from v1.accounts.models import Company
from v1.core.models import Changelog


def index(request):
    return render(request, 'app.html')


class ChangeLogList(TandoraListViewMixin):
    paginate_by = 20
    template_name = 'app.html'

    def get_template_names(self):
        if int(self.request.GET.get('page', 1)) > 1:
            return ['changelog_items.html']
        return ['app.html']

    def get_queryset(self):
        company_id = self.request.session['company-id']
        return Changelog.objects.filter(deleted=False, company__id=company_id).order_by('-created_at')


@is_authenticated
def view_changelog(request, slug):
    try:
        company_id = request.session["company-id"]
        changelog = Changelog.objects.get(company__id=company_id, slug=unquote(slug))
        return render(request, 'single-changelog.html',
                      context={'title': changelog.title, 'content': changelog.content})
    except Changelog.DoesNotExist:
        raise Http404


@transaction.atomic
def view_changelog_as_public(request, company, changelog_terminology, slug):
    try:
        company = get_company_from_slug_and_changelog_terminology(company, changelog_terminology)
        changelog = Changelog.objects.get(company=company, slug=unquote(slug), published=True, deleted=False)
        changelog.view_count += 1
        changelog.save()
        return render(request, 'public/changelog.html',
                      context={'company_name': company.company_name, 'terminology': changelog_terminology,
                               'changelog': changelog,
                               'hide_tandora_logo': True
                               })
    except (Company.DoesNotExist, Changelog.DoesNotExist):
        raise Http404


def public_index(request, company, changelog_terminology):
    try:
        company = get_company_from_slug_and_changelog_terminology(company, changelog_terminology)
        changelogs = Changelog.objects.filter(company=company, deleted=False, published=True).order_by('-created_at')
        return render(request, 'public/index.html',
                      context={'company_name': company.company_name, 'terminology': changelog_terminology,
                               'changelogs': changelogs,
                               'hide_tandora_logo': True})
    except (Company.DoesNotExist, Changelog.DoesNotExist):
        raise Http404
