from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login

from . import forms


def LoginView(request):
    loginForm = forms.LoginForm()

    if request.method == "POST":
        loginForm = forms.LoginForm(request.POST)

        if loginForm.is_valid():
            username = loginForm.cleaned_data['username']
            password = loginForm.cleaned_data['password']

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.add_message(request, messages.SUCCESS, 'Poprawnie zalogowano', 'is-success')
                return redirect('sandbox')
            messages.add_message(request, messages.ERROR, 'Niepoprawne dane logowania', 'is-danger')

    return render(request, 'SKE_USERS/login.html', context={'form': loginForm})
