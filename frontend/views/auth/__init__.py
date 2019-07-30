import uuid

from django.shortcuts import render
from django.urls import reverse

from frontend.constants import COMPANY_CREATED_OR_EDITED_SUCCESSFULLY, COMPANY_DOES_NOT_EXIST
from frontend.custom.decorators import check_auth
from frontend.custom.forms import TandoraForm
from frontend.forms.auth import LoginForm, CompanyForm, UserForm
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
            return render(request, 'login.html', {'token': token, 'is_logged_in': True, 'email': user.email})
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


@check_auth
def logout(request):
    try:
        ClientToken.objects.get(token=request.session["auth-token"]).delete()
    except ClientToken.DoesNotExist:
        pass

    request.session.clear()

    return render(request, 'logout.html')


@check_auth
def profile_form(request):
    email = request.session.get('email', '')
    id = User.objects.get(email=email).id
    return TandoraForm(User, UserForm, 'edit', 'generic-after-login-form.html',
                       reverse('frontend-profile-form')) \
        .get_form(request, id=id)


@check_auth
def company_form(request):
    id = Company.objects.get().id
    return TandoraForm(Company, CompanyForm, 'edit', 'generic-after-login-form.html',
                       reverse('frontend-company-form')) \
        .get_form(request, success_message=COMPANY_CREATED_OR_EDITED_SUCCESSFULLY,
                  error_message=COMPANY_DOES_NOT_EXIST, id=id)
