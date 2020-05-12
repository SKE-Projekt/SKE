from django.shortcuts import render
from django.http import HttpResponse


def SandboxView(request):
    return render(request, 'SKE_SANDBOX/sandbox.html')
