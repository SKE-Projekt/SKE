from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.conf import settings
from django.http import HttpResponseForbidden
from django.template.loader import render_to_string

from . import forms
from . import models


def InvTokenView(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden()
    
    if request.method == "POST":
        form = forms.InvitationTokenForm(request.POST)

        if form.is_valid():
            new_token = models.InvitationToken(email=form.cleaned_data['email'])
            new_token.save()
            messages.add_message(request, messages.SUCCESS, 'Dodano token zaproszeniowy', 'is-success')
        else:
            messages.add_message(request, messages.ERROR, 'Niepoprawne dane', 'is-danger')
    else:
        form = forms.InvitationTokenForm()
    active_tokens = models.InvitationToken.objects.filter(active=True)
    nactive_tokens = models.InvitationToken.objects.filter(active=False)
    return render(request, 'SKE_USERS/inv_tokens.html', context={'form': form, 'atokens': active_tokens, 'ntokens': nactive_tokens})

def SendTokenView(request, id):
    if not request.user.is_superuser:
        return HttpResponseForbidden()
    try:
        token = get_object_or_404(models.InvitationToken, pk=id)
        token.sent = True

        subject = "Udział w testach platformy konkursowej SKE"
        recepient = token.email
        message = render_to_string('SKE_USERS/token_inv.html', context={'token': token})
        send_mail(subject, "", "SKE Projekt <skeprojekt@gmail.com>", [recepient], fail_silently=False, html_message=message)

        token.save()
        messages.add_message(request, messages.SUCCESS, 'Wysłano zaproszenie', 'is-success')
    except Exception as e:
        print("[ERROR]", e, "[END_EMAIL_ERROR]")
        messages.add_message(request, messages.ERROR, 'Błąd podczas wysyłania', 'is-danger')
    return redirect('tokens')

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

def RegisterView(request):
    form = forms.RegisterForm()

    if request.method == "POST":
        form = forms.RegisterForm(request.POST)

        if form.is_valid():
            inv_code = form.cleaned_data['inv_code']
            try:
                token = models.InvitationToken.objects.get(active=True, value=inv_code, email=form.cleaned_data['email'])
            except Exception as e:
                print('[ERROR]', e, '[END_REGIS_ERROR]')
                messages.add_message(request, messages.ERROR, 'Niepoprawny token zaproszeniowy', 'is-danger')
            else:
                form.save()
                token.active = False
                token.save()
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                messages.add_message(request, messages.SUCCESS, 'Konto zostało stworzone', 'is-success')
                return redirect('sandbox')
    return render(request, 'SKE_USERS/register.html', context={'form': form})
