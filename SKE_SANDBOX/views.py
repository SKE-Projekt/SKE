from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required

from . import forms
from . import tasks
from . import models


def InformationView(request):
    return render(request, 'SKE_SANDBOX/information.html')

def SandboxView(request):
    sandboxSubmissionForm = forms.SandboxSubmissionForm()
    try:
        code = models.SandboxSubmission.objects.filter(author=request.user).latest('id').get_code()
    except:
        code = None
    return render(request, 'SKE_SANDBOX/sandbox.html', context={'form': sandboxSubmissionForm, 'code': code})

@login_required
def SubmitSandboxSubmissionView(request):
    sandboxSubmissionForm = forms.SandboxSubmissionForm(request.POST)

    if not sandboxSubmissionForm.is_valid():
        return HttpResponse("ERROR")
    else:
        source_code = sandboxSubmissionForm.cleaned_data['source_code']
        try:
            input_code = sandboxSubmissionForm.cleaned_data['input_code']
        except KeyError:
            input_code = ''
        return HttpResponse('ID:' + str(tasks.checkSandboxSubmissionTask(source_code, input_code, request.user)))

def GetSandboxSubmissionResult(request, id):
    # TODO
    # add form checking for authentication
    submission = get_object_or_404(models.SandboxSubmission, pk=id)

    if submission.author == request.user or request.user.is_authenticated:
        return HttpResponse(submission.result)
    return HttpResponseForbidden('Nie masz pozwolenia na sprawdzenie tego zgłoszenia')

def GetSandboxSubmissionOutput(request, id):
    submission = get_object_or_404(models.SandboxSubmission, pk=id)

    if submission.author == request.user or request.user.is_authenticated:
        return HttpResponse(submission.get_output())
    return HttpResponseForbidden('Nie masz pozwolenia na sprawdzenie tego zgłoszenia')
