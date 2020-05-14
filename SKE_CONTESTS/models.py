import uuid

from django.db import models
from django.contrib.auth import get_user_model


class Contest(models.Model):
    title = models.CharField(max_length=256)
    special_id = models.UUIDField(default=uuid.uuid4)
    date_begin = models.DateTimeField()
    date_end = models.DateTimeField()
    body = models.TextField(max_length=1024*24)

    is_active = models.BooleanField()

class UserContestProfile(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)

class ContestNotification(models.Model):
    title = models.CharField(max_length=256)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    body = models.TextField(max_length=1024 * 24)
    date_published = models.DateTimeField(auto_now_add=True)


# Tasks

class ContestTaskPackageUpload(models.Model):
    RESULT = (
        (0, 'NIE SPRAWDZONA'),
        (1, 'BŁĄD PODCZAS SPRAWDZANIA'),
        (2, 'POPRAWNIE WGRANA')
    )
    
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    path = models.CharField(max_length=1024)
    date_uploaded = models.DateTimeField(auto_now_add=True, editable=False)

    result = models.IntegerField(choices=RESULT, default=0)

class ContestTask(models.Model):
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    package = models.ForeignKey(ContestTaskPackageUpload, on_delete=models.CASCADE)

    ord_id = models.IntegerField()
    timelimit = models.IntegerField()
    sublimit = models.IntegerField()

    body = models.TextField()
    title = models.CharField(max_length=256)
    path = models.CharField(max_length=1024)

class ContestTaskTest(models.Model):
    task = models.ForeignKey(ContestTask, on_delete=models.CASCADE)
    path = models.CharField(max_length=1024)

    ord_id = models.IntegerField()
