from django.contrib import admin

from . import models


admin.site.register(models.Contest)
admin.site.register(models.ContestNotification)
admin.site.register(models.ContestTask)
admin.site.register(models.ContestTaskTest)
admin.site.register(models.ContestTaskPackageUpload)

admin.site.register(models.ContestTaskSubmission)
admin.site.register(models.ContestTaskSubmissionTest)
