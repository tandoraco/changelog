from django.contrib import messages
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response

from frontend.constants import COMPANY_CREATED_OR_EDITED_SUCCESSFULLY, COMPANY_DOES_NOT_EXIST, \
    PASSWORD_RESET_INITIATED, \
    PASSWORD_RESET_SUCCESS, PASSWORD_RESET_TOKEN_INVALID, ACCOUNT_CREATED_MESSAGE, AFFILIATE_CREATED_SUCCESSFULLY, \
    USER_VERIFICATION_FAILED, USER_VERIFICATION_SUCCESS
from frontend.custom.decorators import is_authenticated
from frontend.custom.forms import TandoraForm
from frontend.custom.utils import set_redirect_in_session
from frontend.forms.auth import LoginForm, CompanyForm, UserForm, ForgotPasswordForm, ResetPasswordForm, \
    CompanySignupForm, AffiliateSignupForm
from frontend.forms.auth.utils import clear_request_session, create_session
from frontend.views.auth.utils import save_subscription_details
from v1.accounts.models import User, ClientToken, Company, ForgotPassword, Affiliate, PendingUser
from v1.accounts.serializers import ResetPasswordSerializer


def redirect_to_login_with_message(level, request, message):
    getattr(messages, level)(request, message=message)
    return HttpResponseRedirect("/login")


def login(request):
    redirect_to = request.session.pop('redirect-to', '')

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            create_session(form.data['email'], request)

            if request.user.company.use_case == 's' and request.user.company.is_first_login:
                return HttpResponseRedirect(reverse('frontend-setup-web-builder', args=(1, )))
            if redirect_to:
                return HttpResponseRedirect(redirect_to)

            return HttpResponseRedirect('/staff')
    else:
        clear_request_session(request)
        form = LoginForm()

    set_redirect_in_session(request, redirect_to)

    return render(request, 'login.html', {'form': form})


@is_authenticated
def logout(request):
    try:
        ClientToken.objects.get(token=request.session["auth-token"]).delete()
    except ClientToken.DoesNotExist:
        pass

    clear_request_session(request)

    return render(request, 'logout.html')


def signup(request):
    if request.method == "POST":
        form = CompanySignupForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, message=ACCOUNT_CREATED_MESSAGE)
            return HttpResponseRedirect('/login')
    else:
        form = CompanySignupForm()

    return render(request, 'public/form.html', {
        'form': form,
        'title': 'Signup for 7 day free trial'
    })


def affiliate_signup(request):
    affiliate_content = '''<b>Want to become the Tandora man (affiliate) of Tandora?</b><br>

Becoming a Tandora man is simple but make sure to do loud noises about Tandora. When your noise brings us customers,
you get 12% of the total bill as affiliate charge for every customer you bring in.<br>

<ul>
<li>Hassle-free payments guaranteed.</li>

<li>Payouts on every month.</li>
</ul>
<u>Fill in the below form if you would like to join the Tandora team as Tandora Man:</u>
    '''
    return TandoraForm(Affiliate, AffiliateSignupForm, 'create', 'public/form.html',
                       "/login") \
        .get_form(request, success_message=AFFILIATE_CREATED_SUCCESSFULLY, extra=affiliate_content,
                  title='Affiliate Signup')


@is_authenticated
def profile_form(request):
    email = request.session.get('email', '')
    id = User.objects.get(email=email).id
    return TandoraForm(User, UserForm, 'edit', 'staff/form.html',
                       '/') \
        .get_form(request, id=id)


@is_authenticated
def company_form(request):
    id = request.session["company-id"]
    return TandoraForm(Company, CompanyForm, 'edit', 'staff/form.html',
                       "/login") \
        .get_form(request, success_message=COMPANY_CREATED_OR_EDITED_SUCCESSFULLY,
                  error_message=COMPANY_DOES_NOT_EXIST, id=id)


@api_view(['POST'])
@authentication_classes([])
@transaction.atomic
def razorpay_webhook(request):
    post_data = request.data
    save_subscription_details(post_data)
    return Response('OK')


@transaction.atomic
def forgot_password_form(request):
    return TandoraForm(ForgotPassword, ForgotPasswordForm, 'create', 'public/form.html',
                       "/login") \
        .get_form(request, success_message=PASSWORD_RESET_INITIATED, title="Forgot Password")


@transaction.atomic
def reset_password_form(request, token):
    try:
        ForgotPassword.objects.get(token=token)

        if request.method == "POST":
            form = ResetPasswordForm(request.POST)
            if form.is_valid():
                password = form.cleaned_data.get('password')

                data = {
                    'password': password,
                    'token': token
                }

                serializer = ResetPasswordSerializer(data=data)
                serializer.is_valid()
                # The above will be always true, since we have already form validated the password
                # and we are using token from valid forgot password object
                serializer.save()

                messages.success(request, message=PASSWORD_RESET_SUCCESS)
                return HttpResponseRedirect('/login')
        else:
            form = ResetPasswordForm()

        return render(request, 'public/form.html', {
            'form': form,
            'title': 'Reset Password'
        })
    except ForgotPassword.DoesNotExist:
        return redirect_to_login_with_message('info', request, PASSWORD_RESET_TOKEN_INVALID)


@transaction.atomic
def verify_user(request, token):
    try:
        pending_user = PendingUser.objects.get(uuid=token)

        pending_user.user.is_active = True
        pending_user.user.save()

        pending_user.delete()

        return redirect_to_login_with_message('success', request, USER_VERIFICATION_SUCCESS)
    except PendingUser.DoesNotExist:
        return redirect_to_login_with_message('info', request, USER_VERIFICATION_FAILED)
