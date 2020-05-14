import uuid

from django.db import models
from django.contrib.auth import get_user_model


class Contest(models.Model):
    title = models.CharField(max_length=256)
    special_id = models.UUIDField(default=uuid.uuid4)
    date_begin = models.DateTimeField()
    date_end = models.DateTimeField()
    body = models.TextField(max_length=1024*24)


class ContestNotification(models.Model):
    title = models.CharField(max_length=256)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    body = models.TextField(max_length=1024 * 24)
    date_published = models.DateTimeField(auto_now_add=True)
