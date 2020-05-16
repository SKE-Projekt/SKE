import datetime

from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required

from django.contrib import messages

from . import models
from . import forms
from . import tasks


def ListContests(request):
    active_contests = models.Contest.objects.filter(is_active=True)
    past_contests = models.Contest.objects.filter(is_active=True, date_begin__gt=datetime.datetime.now())
    future_contests = models.Contest.objects.filter(is_active=True, date_end__lt=datetime.datetime.now())
    return render(request, 'SKE_CONTESTS/contests_list.html', context={'active_contests': active_contests, 'future_contests': future_contests, 'past_contests': past_contests})

def ContestDashboard(request, id):
    contest = get_object_or_404(models.Contest, pk=id)
    contest_notifications = models.ContestNotification.objects.filter(contest=contest)
    contest_tasks = models.ContestTask.objects.filter(contest=contest)
     # Coloring tasks
    tasks_passed = []
    tasks_semipassed = []
    tasks_not_passed = []
    tasks_erorrs = []
    if request.user.is_authenticated:
        submissions = models.ContestTaskSubmission.objects.filter(author=request.user, task__contest=contest).order_by('-id')[:6]
        for task in contest_tasks:
            try:
                last_subm = models.ContestTaskSubmission.objects.filter(author=request.user, task=task).latest('id')
                if last_subm.result == 1:
                    tasks_erorrs.append(task.id)
                elif last_subm.result == 2:
                    tasks_not_passed.append(task.id)
                elif last_subm.result == 3:
                    tasks_semipassed.append(task.id)
                elif last_subm.result == 4:
                    tasks_passed.append(task.id)
            except Exception as e:
                print('[ERROR]', e, '[END_CD_ERROR]')
    else:
        submissions = None

    ct_pf = forms.ContestTaskPackageForm()
    return render(request, 'SKE_CONTESTS/contest_dash.html', context={'contest': contest, 'cont_notfis': contest_notifications, 'form': ct_pf, 'tasks': contest_tasks, 'submissions': submissions, 'tpassed': tasks_passed, 'terror': tasks_erorrs, 'tspassed': tasks_semipassed, 'tnpassed': tasks_not_passed})

@login_required
def ListSubmissions(request, id):
    contest = get_object_or_404(models.Contest, pk=id)
    submissions = models.ContestTaskSubmission.objects.filter(author=request.user, task__contest=contest).order_by('-id')
    return render(request, 'SKE_CONTESTS/list_subms.html', {'subms': submissions, 'id': id})

@login_required
def TaskDashboard(request, id):
    task = get_object_or_404(models.ContestTask, pk=id)
    submit_form = forms.ContestTaskSubmissionForm()
    submission_count = models.ContestTaskSubmission.objects.filter(author=request.user, task=task).count()
    submissions = models.ContestTaskSubmission.objects.filter(author=request.user, task=task).order_by('-id')[:6]
    return render(request, 'SKE_CONTESTS/task_dash.html', context={'task': task, 'form': submit_form, 'subms': submissions, 'subms_left': task.sublimit - submission_count})

@login_required
def SubmissionDashboard(request, id):
    subm = get_object_or_404(models.ContestTaskSubmission, pk=id)
    if subm.author == request.user or request.user.is_superuser:
        return render(request, 'SKE_CONTESTS/subm_dash.html', context={'subm': subm})
    return HttpResponseForbidden("Czego tutaj szukasz")

@login_required
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

@login_required
def SendContestTaskSubmission(request, id):
    task = get_object_or_404(models.ContestTask, pk=id)
    form = forms.ContestTaskSubmissionForm(request.POST)
    no_subms_send = models.ContestTaskSubmission.objects.filter(author=request.user, task__contest=task.contest).count()


    if request.method == "POST" and request.user.is_authenticated and form.is_valid():
        if no_subms_send >= task.sublimit and not request.user.is_superuser:
            messages.add_message(request, messages.ERROR, 'Przekroczyłeś limit zgłoszeń dla danego zadania', 'is-danger')
        else:
            tasks.SaveTaskSubmission(form.cleaned_data['code'], request.user, task)
            messages.add_message(request, messages.SUCCESS, 'Poprawnie przesłano zgłoszenie', 'is-success')
    else:
        messages.add_message(request, messages.ERROR, 'Nie udało się przesłać zgłoszenia', 'is-danger')
    return redirect("ContestDashboard", id=task.contest.id)
