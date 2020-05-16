from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(max_length=96, required=True)
    password = forms.CharField(max_length=96, required=True, widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'input is-primary'

class RegisterForm(UserCreationForm):
    inv_code = forms.CharField(max_length=10, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'inv_code')

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'input is-primary'

class InvitationTokenForm(forms.Form):
    email = forms.EmailField()

    
    def __init__(self, *args, **kwargs):
        super(InvitationTokenForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'input is-primary'
