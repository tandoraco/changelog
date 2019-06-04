import uuid

from django.shortcuts import render

from frontend.forms.auth import LoginForm
from v1.accounts.models import User, ClientToken


def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = User.objects.get(email=form.data['email'])
            token = str(uuid.uuid4())
            ClientToken.objects.create(token=token, user=user)
            return render(request, 'app.html', {'token': token, 'is_logged_in': True, 'email': user.email})
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def logout(request):
    pass
