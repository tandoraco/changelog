import uuid

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.text import slugify

from frontend.constants import COMPANY_CREATED_OR_EDITED_SUCCESSFULLY, COMPANY_DOES_NOT_EXIST
from frontend.custom.decorators import is_authenticated
from frontend.custom.forms import TandoraForm
from frontend.forms.auth import LoginForm, CompanyForm, UserForm
from frontend.forms.auth.utils import clear_request_session
from v1.accounts.models import User, ClientToken, Company


def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = User.objects.get(email=form.data['email'])
            token = str(uuid.uuid4())
            ClientToken.objects.create(token=token, user=user)
            request.session["auth-token"] = token
            request.session["email"] = user.email
            request.session["user-id"] = user.id
            request.session["company-id"] = user.company.id

            company_slug = slugify(user.company.company_name)
            changelog_terminology = slugify(user.company.changelog_terminology)
            request.session["public-page-url"] = f'/{company_slug}/{changelog_terminology}'
            return HttpResponseRedirect('/staff/changelogs')
    else:
        clear_request_session(request)
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


@is_authenticated
def logout(request):
    try:
        ClientToken.objects.get(token=request.session["auth-token"]).delete()
    except ClientToken.DoesNotExist:
        pass

    clear_request_session(request)

    return render(request, 'logout.html')


@is_authenticated
def profile_form(request):
    email = request.session.get('email', '')
    id = User.objects.get(email=email).id
    return TandoraForm(User, UserForm, 'edit', 'generic-after-login-form.html',
                       '/') \
        .get_form(request, id=id)


@is_authenticated
def company_form(request):
    id = request.session["company-id"]
    return TandoraForm(Company, CompanyForm, 'edit', 'generic-after-login-form.html',
                       "/login") \
        .get_form(request, success_message=COMPANY_CREATED_OR_EDITED_SUCCESSFULLY,
                  error_message=COMPANY_DOES_NOT_EXIST, id=id)
