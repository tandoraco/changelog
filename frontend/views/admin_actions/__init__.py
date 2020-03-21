from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required
from django.core.management import call_command
from django.http import HttpResponseRedirect

from frontend.views.admin_actions.utils import super_user_and_admin


@login_required
@user_passes_test(super_user_and_admin)
def delete_company(request, company_name):
    try:
        call_command('delete_company', company_name)
        messages.success(request, message='Company deleted successfully.')
    except Exception as e:
        messages.error(request, message=f'Unable to delete the company. Exception: {e.__repr__()}')

    return HttpResponseRedirect('/admin/v1/company/')
