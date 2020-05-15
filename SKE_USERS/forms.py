from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(max_length=96, required=True)
    password = forms.CharField(max_length=96, required=True)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'input is-primary'

class InvitationTokenForm(forms.Form):
    email = forms.EmailField()

    
    def __init__(self, *args, **kwargs):
        super(InvitationTokenForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'input is-primary'
