from django.db import models
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
