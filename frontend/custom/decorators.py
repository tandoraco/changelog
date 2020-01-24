import functools

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

from frontend.constants import FREE_TRIAL_EXPIRED, NOT_ALLOWED, PLAN_LIMIT_REACHED_MESSAGE
from frontend.custom.utils import redirect_to_login
from frontend.forms.auth.utils import is_valid_auth_token_and_email, is_trial_expired, DEFAULT_PLAN_FEATURES
from v1.accounts.models import Company
from v1.categories.models import Category
from v1.core.models import Changelog


def is_authenticated(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        request = args[0]

        if is_trial_expired(request):
            messages.error(request, message=FREE_TRIAL_EXPIRED)
            return redirect_to_login(request)

        if not is_valid_auth_token_and_email(request):
            return redirect_to_login(request)

        return func(*args, **kwargs)

    return wrapper


def requires_static_site(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        request = args[0]
        company_id = request.session['company-id']
        company = Company.objects.get(id=company_id)

        if not company.is_static_site:
            messages.warning(request, NOT_ALLOWED)
            return HttpResponseRedirect('/staff')

        return func(*args, **kwargs)

    return wrapper


def is_limit_reached(feature_name, plan_features, company_id):
    model = None
    if feature_name == 'changelogs':
        model = Changelog
    elif feature_name == 'categories':
        model = Category

    if model:
        count = len(model.objects.filter(company_id=company_id, deleted=False))
        return not count < plan_features.get(feature_name)
    else:
        return False


def is_allowed(feature_name):

    def real_decorator(func):

        def wrapper(*args, **kwargs):
            request = args[0]
            company_id = request.session["company-id"]
            try:
                plan_features = request.session['plan-features']
            except KeyError:
                plan_features = DEFAULT_PLAN_FEATURES

            if feature_name in {'changelogs', 'categories'} and is_limit_reached(
                    feature_name, plan_features, company_id):
                messages.info(request, PLAN_LIMIT_REACHED_MESSAGE)
                return HttpResponseRedirect(reverse('frontend-staff-index'))

            return func(*args, **kwargs)

        return wrapper

    return real_decorator
