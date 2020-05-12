import uuid

from django.db import models
from django.contrib.auth import get_user_model


class SandboxSubmission(models.Model):
    RESULT = (
        (0, 'NIE SPRAWDZONO'),
        (1, 'BŁĄD SPRAWDZANIA'),
        (2, 'BŁĄD WYKONANIA'),
        (3, 'POPRAWNIE WYKONANO')
    )

    special_id = models.UUIDField(default=uuid.uuid4, editable=False)
    submission_date = models.DateTimeField(auto_now_add=True, editable=False)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, editable=False)

    result = models.IntegerField(default=0, choices=RESULT)
