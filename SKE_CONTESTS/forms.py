from django import forms


class ContestTaskPackageForm(forms.Form):
    package_file = forms.FileField()

    def __init__(self, *args, **kwargs):
        super(ContestTaskPackageForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'file-input is-warning'

class ContestTaskSubmissionForm(forms.Form):
    code = forms.CharField(widget=forms.Textarea, max_length=24 * 1024)
