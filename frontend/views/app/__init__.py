import uuid
from urllib.parse import unquote

from django.contrib import messages
from django.db import transaction
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils.text import slugify

from frontend import constants as frontend_constants
from frontend.constants import PASSWORD_RESET_INITIATED
from frontend.custom import views as custom_views
from frontend.custom.decorators import is_authenticated, is_admin, is_allowed
from frontend.custom.forms import TandoraForm
from frontend.custom.utils import get_company_from_slug_and_changelog_terminology, \
    get_changelogs_from_company_name_and_changelog_terminology, get_public_changelog_limit
from frontend.forms.auth import UserForm, StaffNewUserForm
from frontend.views.app.public_helpers import get_context_and_template_name, render_custom_theme
from v1.accounts.constants import INACTIVE_USER_ADMIN_ERROR
from v1.accounts.models import Company, User, ForgotPassword
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
        return Changelog.objects.filter(deleted=False, company__id=company_id).select_related().order_by('-created_at')


@is_authenticated
def view_changelog(request, slug):
    try:
        company_id = request.session["company-id"]
        changelog = Changelog.objects.get(company__id=company_id, slug=unquote(slug), deleted=False)
        return render(request, 'staff/changelogs/changelog.html',
                      context={'changelog': changelog})
    except Changelog.DoesNotExist:
        raise Http404


def company_public_index(request, company):
    company = unquote(company.replace('-', ' '))
    company_object = get_object_or_404(Company, company_name__iexact=company)
    company = company.lower()
    return HttpResponseRedirect(f'/{slugify(company)}/{company_object.changelog_terminology.lower().replace(" ", "-")}')


@transaction.atomic
def view_changelog_as_public(request, company, changelog_terminology, slug):
    try:
        company_name = company
        changelogs = get_changelogs_from_company_name_and_changelog_terminology(company_name, changelog_terminology)
        changelog = changelogs.filter(slug=unquote(slug)).select_related('company', 'company__subscription')[0]
        company = changelog.company

        context, template = get_context_and_template_name(company, changelog=True)
        if context.get('config'):
            context['config']['home_page_title'] = changelog.title
            context['config']['home_page_content'] = changelog.content
            return render_custom_theme(company, context, request)
        else:
            context.update({'changelog': changelog})
            return render(request, template, context=context)

    except (Company.DoesNotExist, Changelog.DoesNotExist, IndexError):
        raise Http404


def view_changelog_custom_url(request):
    try:
        request_path = request.path.strip('/')
        request_path_parts = request_path.split('/')
        company = unquote(request_path_parts[0]).replace('-', ' ')
        custom_path = '/'.join(request_path_parts[1:])
        if not custom_path:
            raise Http404
        changelog = Changelog.objects.filter(company__company_name__iexact=company,
                                             custom_url_path__iexact=custom_path,
                                             deleted=False).select_related()[0]
        context, template = get_context_and_template_name(changelog.company, changelog=True)
        if context.get('config'):
            context['config']['home_page_title'] = changelog.title
            context['config']['home_page_content'] = changelog.content
            return render_custom_theme(changelog.company, context, request)
        else:
            context.update({'changelog': changelog})
            return render(request, template, context=context)
    except IndexError:
        raise Http404


def public_index(request, company, changelog_terminology):
    try:
        company_name = company
        changelogs = get_changelogs_from_company_name_and_changelog_terminology(company_name, changelog_terminology)
        company = None
        for changelog in changelogs:
            # Why I am iterating here instead of taking the company from index[0]
            # when all changelogs belong to one company ?
            # Reason: Django evaluates queryset lazily
            # So when I take company from index 0, only one object from queryset is evaluated
            # and when rendering in template queryset is again evaluated
            # which makes the number of db calls to 2.
            # So hacking this behaviour to evaluate the queryset only once and
            # keep the db call to 1
            company = changelog.company
        if not company:
            # changes for back-portability
            # when there are no published pages/changelogs but static site config is present
            # this is required to render the website
            company = get_company_from_slug_and_changelog_terminology(company_name, changelog_terminology)
            changelogs = Changelog.objects.filter(company=company, deleted=False, published=True).order_by(
                '-created_at').select_related('category')

        context, template = get_context_and_template_name(company)
        context['changelog_limit'] = get_public_changelog_limit(company)
        if context.get('config'):
            context['config']['home_page_title'] = ''
            return render_custom_theme(company, context, request)
        else:
            context['changelogs'] = changelogs
            return render(request, template, context=context)

    except (Company.DoesNotExist, Changelog.DoesNotExist, IndexError):
        raise Http404


class UserList(custom_views.TandoraAdminListViewMixin):
    template_name = 'staff/users/index.html'

    def get_queryset(self):
        from v1.accounts.models import User
        company_id = self.request.session['company-id']
        return User.objects.filter(company__id=company_id).exclude(id=self.request.user.id)


@is_authenticated
@is_admin
@is_allowed('users', redirect_to='frontend-view-users')
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
                       reverse('frontend-view-users')) \
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


@is_authenticated
@is_admin
def reset_password(request, id):
    user = get_object_or_404(User, pk=id, company_id=request.session['company-id'])

    if not user.is_active:
        messages.warning(request, INACTIVE_USER_ADMIN_ERROR)
    else:
        # First delete, previous password reset tokens and reset the password.
        ForgotPassword.objects.filter(email=user.email).delete()
        ForgotPassword.objects.create(email=user.email, token=str(uuid.uuid4()))
        messages.success(request, PASSWORD_RESET_INITIATED.replace('You', str(user)))

    return HttpResponseRedirect(reverse('frontend-view-users'))
