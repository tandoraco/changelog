import functools
import json

from django.apps import apps
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

from frontend.constants import FREE_TRIAL_EXPIRED, NOT_ALLOWED, PLAN_LIMIT_REACHED_MESSAGE, \
    ONLY_ADMIN_CAN_PERFORM_THIS_ACTION_ERROR
from frontend.custom.utils import redirect_to_login
from frontend.forms.auth.utils import is_valid_auth_token_and_email, is_trial_expired, DEFAULT_PLAN_FEATURES
from v1.accounts.models import Company


def feature_with_integer_limits(features):
    _features = set()

    for feature_name, feature_limit in features.items():
        try:
            # boolean values are also treated as int
            # so isinstance(feature_limit, int) will return true, when it is either bool or int
            # So first converting the feature_limit to str and then converting back to int
            # this will throw ValueError if the feature_limit is not int
            int(str(feature_limit))
            _features.add(feature_name)
        except ValueError:
            pass

    return _features


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


def is_admin(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        request = args[0]

        if request.user.company.admin == request.user:
            return func(*args, **kwargs)
        else:
            messages.warning(request, ONLY_ADMIN_CAN_PERFORM_THIS_ACTION_ERROR)
            return HttpResponseRedirect('/staff')

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
    # Feature name will be in plural and lower case.
    # So removing s from the end and title casing would give the model name
    model_name = feature_name[:-1].title()
    model = apps.get_model('v1', model_name)

    if hasattr(model, 'deleted'):
        count = len(model.objects.filter(company_id=company_id, deleted=False))
    else:
        count = len(model.objects.filter(company_id=company_id))

    return not count < plan_features.get(feature_name)


def is_allowed(feature_name, redirect_to=None):

    def real_decorator(func):

        def wrapper(*args, **kwargs):
            request = args[0]
            company_id = request.session["company-id"]

            subscription = request.user.company.subscription
            if subscription and subscription.plan and subscription.plan.plan_features:
                plan_features = json.loads(subscription.plan.plan_features)

                if subscription.extra_plan_features:
                    plan_features.update(json.loads(subscription.extra_plan_features))

                for default_feature_name, default_feature_limit in DEFAULT_PLAN_FEATURES.items():
                    if default_feature_name not in plan_features:
                        plan_features[default_feature_name] = default_feature_limit
            else:
                plan_features = DEFAULT_PLAN_FEATURES

            if feature_name in feature_with_integer_limits(plan_features) and is_limit_reached(
                    feature_name, plan_features, company_id):
                messages.info(request, PLAN_LIMIT_REACHED_MESSAGE)
                if not redirect_to:
                    return HttpResponseRedirect(reverse('frontend-staff-index'))
                else:
                    return HttpResponseRedirect(reverse(redirect_to))

            return func(*args, **kwargs)

        return wrapper

    return real_decorator
