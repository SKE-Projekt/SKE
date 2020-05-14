import os
import uuid

from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model


class CourseUpload(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)
    date_uploaded = models.DateTimeField(auto_now_add=True)
    path = models.CharField(max_length=1024)

    result = models.IntegerField()

class Course(models.Model):
    title = models.CharField(max_length=256)
    ord_id = models.IntegerField()
    father_course = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True)
    upload = models.ForeignKey(CourseUpload, on_delete=models.CASCADE)
    body_md = models.TextField(max_length=24 * 1024)
    body_html = models.TextField(max_length=48 * 1024, blank=True)

class CourseExercise(models.Model):
    title = models.CharField(max_length=256)
    ord_id = models.IntegerField()
    path = models.CharField(max_length=1024)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    start_code = models.TextField(max_length=24 * 1024)
    body_md = models.TextField(max_length=24 * 1024)
    body_html = models.TextField(max_length=48 * 1024, blank=True)

    def get_example(self):
        courses_path = os.path.join(settings.FILES_DIR, 'SKE_COURSES')
        exer_path = os.path.join(courses_path, self.path)
        exer_example_path = os.path.join(exer_path, 'przyklad.ed')
        with open(exer_example_path, 'r+', encoding='utf-8') as f:
            return f.read()

class ExerciseSubmission(models.Model):
    RESULT = (
        (0, 'NIE SPRAWDZONO'),
        (1, 'BŁĄD SPRAWDZANIA'),
        (2, 'BŁĄD WYKONANIA'),
        (3, 'BŁĘDNY WYNIK'),
        (4, 'POPRAWNY WYNIK')
    )

    special_id = models.UUIDField(default=uuid.uuid4, editable=False)
    submission_date = models.DateTimeField(auto_now_add=True, editable=False)

    code = models.TextField(max_length=24 * 1024, editable=False)
    exercise = models.ForeignKey(CourseExercise, on_delete=models.CASCADE, editable=False)

    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, editable=False)
    result = models.IntegerField(default=0, choices=RESULT)

class ExerciseExampleShowing(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    exercise = models.ForeignKey(CourseExercise, on_delete=models.CASCADE)

    date = models.DateTimeField(auto_now_add=True)


# class SandboxSubmission(models.Model):
#     RESULT = (
#         (0, 'NIE SPRAWDZONO'),
#         (1, 'BŁĄD SPRAWDZANIA'),
#         (2, 'BŁĄD WYKONANIA'),
#         (3, 'POPRAWNIE WYKONANO')
#     )

#     special_id = models.UUIDField(default=uuid.uuid4, editable=False)
#     submission_date = models.DateTimeField(auto_now_add=True, editable=False)
#     author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, editable=False)

#     result = models.IntegerField(default=0, choices=RESULT)

#     def get_output(self):
#         outputPath = os.path.join(os.path.join(settings.FILES_DIR, 'SKE_SANDBOX'), str(self.special_id))
#         with open(os.path.join(outputPath, 'output.out'), 'r+', encoding='utf-8') as f:
#             output_code = f.read()
#         return output_code