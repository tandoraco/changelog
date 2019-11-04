from datetime import timedelta

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.utils import timezone

from frontend.constants import NOT_LOGGED_IN_ERROR, FREE_TRIAL_PERIOD_IN_DAYS, LOGIN_AGAIN_INFO,\
    TRIAL_UPGRADE_WARNING, TRIAL_ENDS_TODAY
from v1.accounts.models import ClientToken, Company


def is_valid_auth_token_and_email(request):
    token = request.session.get("auth-token", None)
    email = request.session.get("email", None)

    if not (token or email):
        return False

    try:
        ct = ClientToken.objects.get(token=token)
        assert ct.user.email == email
        assert request.session["user-id"]
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
        return HttpResponseRedirect('/login')

    now = timezone.now()
    if company.is_trial_account and (company.created_time + timedelta(days=FREE_TRIAL_PERIOD_IN_DAYS) < now):
        return True

    if company.is_trial_account:
        days_left_in_trial = ((company.created_time + timedelta(days=FREE_TRIAL_PERIOD_IN_DAYS)) - now).days
        if days_left_in_trial == 0:
            messages.warning(request, message=TRIAL_ENDS_TODAY, fail_silently=True)
        elif days_left_in_trial > 0:
            messages.info(request, message=TRIAL_UPGRADE_WARNING.format(days=days_left_in_trial), fail_silently=True)
    return False
