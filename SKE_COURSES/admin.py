from django.contrib import admin

# Register your models here.
from . import models

admin.site.register(models.Course)
admin.site.register(models.CourseUpload)
admin.site.register(models.CourseExercise)
admin.site.register(models.ExerciseSubmission)
admin.site.register(models.ExerciseExampleShowing)