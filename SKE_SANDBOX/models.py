import os
import uuid

from django.db import models
from django.conf import settings
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

    def get_output(self):
        outputPath = os.path.join(os.path.join(settings.FILES_DIR, 'SKE_SANDBOX'), str(self.special_id))
        with open(os.path.join(outputPath, 'output.out'), 'r+', encoding='utf-8') as f:
            output_code = f.read()
        os.system(f"rm {os.path.join(outputPath, 'output.out')}")
        return output_code
    
    def get_code(self):
        codePath = os.path.join(os.path.join(settings.FILES_DIR, 'SKE_SANDBOX'), str(self.special_id))
        with open(os.path.join(codePath, 'source.ed'), 'r+', encoding='utf-8') as f:
            code = f.read()
        return code
