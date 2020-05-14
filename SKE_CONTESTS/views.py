import datetime

from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden

from django.contrib import messages

from . import models
from . import forms
from . import tasks


def ListContests(request):
    active_contests = models.Contest.objects.filter(is_active=True)
    past_contests = models.Contest.objects.filter(is_active=False, date_begin__gt=datetime.datetime.now())
    future_contests = models.Contest.objects.filter(is_active=False, date_end__lt=datetime.datetime.now())
    return render(request, 'SKE_CONTESTS/contests_list.html', context={'active_contests': active_contests, 'future_contests': future_contests, 'past_contests': past_contests})

def ContestDashboard(request, id):
    contest = get_object_or_404(models.Contest, pk=id)
    contest_notifications = models.ContestNotification.objects.filter(contest=contest)

    contest_tasks = models.ContestTask.objects.filter(contest=contest)

    ct_pf = forms.ContestTaskPackageForm()
    return render(request, 'SKE_CONTESTS/contest_dash.html', context={'contest': contest, 'cont_notfis': contest_notifications, 'form': ct_pf, 'tasks': contest_tasks})

def TaskDashboard(request, id):
    task = get_object_or_404(models.ContestTask, pk=id)
    return render(request, 'SKE_CONTESTS/task_dash.html', context={'task': task})

def UploadContestTaskPackage(request, id):
    if request.user.is_superuser:
        contest = get_object_or_404(models.Contest, pk=id)

        form = forms.ContestTaskPackageForm(request.POST, request.FILES)
        if form.is_valid():
            tasks.UploadContestTaskPackage(request.FILES['package_file'], request.user, contest)
            messages.add_message(request, messages.SUCCESS, 'Poprawnie przesłano paczkę', 'is-success')
        else:
            messages.add_message(request, messages.SUCCESS, 'Nie przesłano paczki', 'is-danger')
        return redirect('ContestDashboard', id=id)
    return HttpResponseForbidden()