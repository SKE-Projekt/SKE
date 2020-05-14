import datetime

from django.shortcuts import render

from . import models


def ListContests(request):
    active_contests = models.Contest.objects.filter(is_active=True)
    past_contests = models.Contest.objects.filter(is_active=False, date_begin__gt=datetime.datetime.now())
    future_contests = models.Contest.objects.filter(is_active=False, date_end__lt=datetime.datetime.now())
    return render(request, 'SKE_CONTESTS/contests_list.html', context={'active_contests': active_contests, 'future_contests': future_contests, 'past_contests': past_contests})
