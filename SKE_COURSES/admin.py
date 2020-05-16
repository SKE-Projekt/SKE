from django.contrib import admin

from django.db.models import ManyToOneRel, ForeignKey, OneToOneField

from . import models

MySpecialAdmin = lambda model: type('SubClass'+model.__name__, (admin.ModelAdmin,), {
        'list_display': [x.name for x in model._meta.fields],
            'list_select_related': [x.name for x in model._meta.fields if isinstance(x, (ManyToOneRel, ForeignKey, OneToOneField,))]
            })

admin.site.register(models.Course)
admin.site.register(models.CourseUpload)
admin.site.register(models.CourseExercise)
admin.site.register(models.ExerciseSubmission, MySpecialAdmin(models.ExerciseSubmission))
admin.site.register(models.ExerciseExampleShowing, MySpecialAdmin(models.ExerciseExampleShowing))
