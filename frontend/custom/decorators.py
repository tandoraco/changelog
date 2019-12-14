import functools

from django.contrib import messages
from django.http import HttpResponseRedirect

from frontend.constants import FREE_TRIAL_EXPIRED, NOT_ALLOWED
from frontend.custom.utils import redirect_to_login
from frontend.forms.auth.utils import is_valid_auth_token_and_email, is_trial_expired
from v1.accounts.models import Company


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
            messages.info(request, NOT_ALLOWED)
            return HttpResponseRedirect('/')

        return func(*args, **kwargs)

    return wrapper
