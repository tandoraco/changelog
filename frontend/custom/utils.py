import json

from django.contrib import messages as msgs
from django.contrib.messages import get_messages
from django.http import HttpResponseRedirect

from v1.accounts.models import Company


def delete_model(request, model, id, success_redirect_path, error_redirect_path, success_message, error_message):
    try:
        instance = model.objects.get(id=id)
        if hasattr(instance, 'deleted'):
            setattr(instance, 'deleted', True)
            instance.save()
        else:
            instance.delete()

        msgs.success(request, message=success_message)
    except model.DoesNotExist:
        msgs.error(request, message=error_message)
        return HttpResponseRedirect(error_redirect_path)

    return HttpResponseRedirect(success_redirect_path)


def get_company_from_slug_and_changelog_terminology(company, changelog_terminology):
    company = company.replace("-", " ")
    changelog_terminology = changelog_terminology.replace("-", " ")
    company = Company.objects.get(company_name__iexact=company, changelog_terminology__iexact=changelog_terminology)
    return company


def get_company_from_request(request):
    company_id = request.session['company-id']
    return Company.objects.get(id=company_id)


def save_and_get_redirect_url(request):
    redirect_to = request.path
    request.session['redirect-to'] = redirect_to
    return redirect_to


def redirect_to_login(request):
    redirect_to = save_and_get_redirect_url(request)
    # Showing redirect url in path for transparency
    # Saving redirect to in request session, so that unsafe url redirects can be avoided
    return HttpResponseRedirect(f'/login?redirect_to={redirect_to}')


def set_redirect_in_session(request, redirect_to):
    if redirect_to:
        request.session['redirect-to'] = redirect_to


def messages(request):
    """Remove duplicate messages"""
    _messages = []
    unique_messages = []
    for m in get_messages(request):
        if m.message not in _messages:
            _messages.append(m.message)
            unique_messages.append(m)

    return {'messages': unique_messages}


class SettingsMixin(object):

    @property
    def settings(self):
        return json.loads(self._settings) if self._settings else {}

    @settings.setter
    def settings(self, value):
        self._settings = json.dumps(value)
