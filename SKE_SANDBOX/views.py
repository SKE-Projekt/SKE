from django.shortcuts import render
from django.http import HttpResponse

from . import forms
from . import tasks


def SandboxView(request):
    sandboxSubmissionForm = forms.SandboxSubmissionForm()
    return render(request, 'SKE_SANDBOX/sandbox.html', context={'form': sandboxSubmissionForm})

def SubmitSandboxSubmissionView(request):
    print(request.POST)
    sandboxSubmissionForm = forms.SandboxSubmissionForm(request.POST)

    if sandboxSubmissionForm.is_valid():
        return HttpResponse("ERROR")
    else:
        source_code = sandboxSubmissionForm.cleaned_data['source_code']
        try:
            input_code = sandboxSubmissionForm.cleaned_data['input_code']
        except KeyError:
            input_code = ''
        return HttpResponse(tasks.checkSandboxSubmissionTask(source_code, input_code, request.user))
