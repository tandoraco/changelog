from urllib.parse import unquote

from django.contrib import messages
from django.db import transaction
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from frontend import constants as frontend_constants
from frontend.custom.decorators import is_authenticated, is_admin
from frontend.custom.forms import TandoraForm
from frontend.custom.utils import get_company_from_slug_and_changelog_terminology
from frontend.custom import views as custom_views
from frontend.forms.auth import UserForm, StaffNewUserForm
from frontend.views.app.public_helpers import get_context_and_template_name, render_custom_theme
from v1.accounts.models import Company, User
from v1.core.models import Changelog


def index(request):
    return render(request, 'app.html')


class ChangeLogList(custom_views.TandoraListViewMixin):
    paginate_by = 20
    template_name = 'app.html'

    def get_template_names(self):
        if int(self.request.GET.get('page', 1)) > 1:
            return ['staff/changelogs/index.html']
        return ['app.html']

    def get_queryset(self):
        company_id = self.request.session['company-id']
        return Changelog.objects.filter(deleted=False, company__id=company_id).order_by('-created_at')


@is_authenticated
def view_changelog(request, slug):
    try:
        company_id = request.session["company-id"]
        changelog = Changelog.objects.get(company__id=company_id, slug=unquote(slug), deleted=False)
        return render(request, 'staff/changelogs/changelog.html',
                      context={'title': changelog.title, 'content': changelog.content})
    except Changelog.DoesNotExist:
        raise Http404


def company_public_index(request, company):
    company_object = get_object_or_404(Company, company_name__iexact=company)
    company = company.lower()
    return HttpResponseRedirect(f'/{company}/{company_object.changelog_terminology.lower().replace(" ", "-")}')


@transaction.atomic
def view_changelog_as_public(request, company, changelog_terminology, slug):
    try:
        company = get_company_from_slug_and_changelog_terminology(company, changelog_terminology)
        changelog = Changelog.objects.get(company=company, slug=unquote(slug), published=True, deleted=False)
        changelog.view_count += 1
        changelog.save()

        context, template = get_context_and_template_name(company, changelog=True)
        if context.get('config'):
            context['config']['home_page_title'] = changelog.title
            context['config']['home_page_content'] = changelog.content
            return render_custom_theme(company, context, request)
        else:
            context.update({'changelog': changelog})
            return render(request, template, context=context)

    except (Company.DoesNotExist, Changelog.DoesNotExist):
        raise Http404


def public_index(request, company, changelog_terminology):
    try:
        company = get_company_from_slug_and_changelog_terminology(company, changelog_terminology)
        changelogs = Changelog.objects.filter(company=company, deleted=False, published=True).order_by('-created_at')

        context, template = get_context_and_template_name(company)
        if context.get('config'):
            context['config']['home_page_title'] = ''
            return render_custom_theme(company, context, request)
        else:
            context['changelogs'] = changelogs
            return render(request, template, context=context)

    except (Company.DoesNotExist, Changelog.DoesNotExist):
        raise Http404


class UserList(custom_views.TandoraAdminListViewMixin):
    template_name = 'staff/users/index.html'

    def get_queryset(self):
        from v1.accounts.models import User
        company_id = self.request.session['company-id']
        return User.objects.filter(company__id=company_id).exclude(id=self.request.user.id)


@is_authenticated
@is_admin
def create_user(request):
    initial = {
        'company': request.user.company
    }
    return TandoraForm(User, StaffNewUserForm, 'create', 'staff/form.html',
                       reverse('frontend-view-users'), initial=initial) \
        .get_form(request,
                  success_message=frontend_constants.USER_CREATED_OR_EDITED_SUCCESSFULLY,
                  error_message=frontend_constants.USER_DOES_NOT_EXIST)


@is_authenticated
@is_admin
def edit_user(request, id):
    return TandoraForm(User, UserForm, 'edit', 'staff/form.html',
                       reverse('frontend-view-users'))\
        .get_form(request,
                  success_message=frontend_constants.USER_CREATED_OR_EDITED_SUCCESSFULLY,
                  error_message=frontend_constants.USER_DOES_NOT_EXIST, id=id)


def _set_user_is_active(is_active, id):
    user = get_object_or_404(User, pk=id)
    user.is_active = is_active
    user.save()


@is_authenticated
@is_admin
def deactivate_user(request, id):
    _set_user_is_active(False, id)
    messages.success(request, message=frontend_constants.USER_DEACTIVATED_SUCCESSFULLY)
    return HttpResponseRedirect(reverse('frontend-view-users'))


@is_authenticated
@is_admin
def activate_user(request, id):
    _set_user_is_active(True, id)
    messages.success(request, message=frontend_constants.USER_ACTIVATED_SUCCESSFULLY)
    return HttpResponseRedirect(reverse('frontend-view-users'))
