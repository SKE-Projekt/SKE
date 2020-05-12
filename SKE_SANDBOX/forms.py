from django import forms


class SandboxSubmissionForm(forms.Form):
    source_code = forms.CharField(max_length=(24 * 1024), required=True)
    input_code = forms.CharField(max_length=(24 * 1024))
