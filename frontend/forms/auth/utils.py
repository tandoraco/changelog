import json
import uuid
from datetime import timedelta

from django.conf import settings
from django.contrib import messages
from django.utils import timezone
from django.utils.text import slugify

from frontend.constants import NOT_LOGGED_IN_ERROR, FREE_TRIAL_PERIOD_IN_DAYS, LOGIN_AGAIN_INFO, \
    TRIAL_UPGRADE_WARNING, TRIAL_ENDS_TODAY
from v1.accounts.constants import INACTIVE_USER_ERROR
from v1.accounts.models import ClientToken, Company, User, Subscription

CHANGELOG_TESTING_LIMIT = 5
DEFAULT_PLAN_FEATURES = {
    'changelogs': 500 if not settings.TESTING else CHANGELOG_TESTING_LIMIT,
    'categorys': 5,
    'show_tandora_branding_at_footer': True,
    'users': 1
}


def is_valid_auth_token_and_email(request):
    token = request.session.get("auth-token", None)
    email = request.session.get("email", None)

    if not (token or email):
        return False

    try:
        ct = ClientToken.objects.get(token=token)
        assert ct.user.email == email
        assert request.session["user-id"]
        request.user = ct.user

        if not request.user.is_active:
            messages.error(request, message=INACTIVE_USER_ERROR)
            return False
    except (ClientToken.DoesNotExist, AssertionError):
        messages.error(request, message=NOT_LOGGED_IN_ERROR)
        return False

    return True


def clear_request_session(request):
    request.session.clear()
    request.session.flush()


def is_trial_expired(request):
    try:
        company = Company.objects.get(id=request.session['company-id'])
    except KeyError:
        messages.info(request, message=LOGIN_AGAIN_INFO, fail_silently=True)
        return False

    now = timezone.now()
    if company.is_trial_account and (now > company.created_time + timedelta(days=FREE_TRIAL_PERIOD_IN_DAYS)):
        return True

    if company.is_trial_account:
        days_left_in_trial = ((company.created_time + timedelta(days=FREE_TRIAL_PERIOD_IN_DAYS)) - now).days
        if days_left_in_trial == 0:
            messages.warning(request, message=TRIAL_ENDS_TODAY, fail_silently=True)
        elif days_left_in_trial > 0 and (days_left_in_trial < FREE_TRIAL_PERIOD_IN_DAYS - 3):
            messages.info(request, message=TRIAL_UPGRADE_WARNING.format(days=days_left_in_trial), fail_silently=True)
    return False


def get_plan_features(company_id, company=None):
    try:
        if not company:
            subscription = Subscription.objects.get(company_id=company_id)
        else:
            subscription = company.subscription
        plan_features = json.loads(subscription.plan.plan_features)
    except Subscription.DoesNotExist:
        subscription = None
        plan_features = DEFAULT_PLAN_FEATURES

    if subscription and subscription.extra_plan_features:
        plan_features.update(json.loads(subscription.extra_plan_features))

    for plan_feature in DEFAULT_PLAN_FEATURES:
        if plan_feature not in plan_features:
            plan_features[plan_feature] = DEFAULT_PLAN_FEATURES[plan_feature]

    return plan_features


def create_session(email, request):
    user = User.objects.get(email=email)
    token = str(uuid.uuid4())
    ClientToken.objects.create(token=token, user=user)
    request.session["auth-token"] = token
    request.session["email"] = user.email
    request.session["user-id"] = user.id
    request.session["company-id"] = user.company.id
    company_slug = slugify(user.company.company_name)
    changelog_terminology = slugify(user.company.changelog_terminology)
    request.session["public-page-url"] = f'/{company_slug}/{changelog_terminology}'
