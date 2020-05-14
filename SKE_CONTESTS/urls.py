from django.urls import path

from . import views


urlpatterns = [
    path('', views.ListContests, name='ListContests'),
    path('contest/<int:id>', views.ContestDashboard, name='ContestDashboard'),
    path('contest/task/<int:id>', views.TaskDashboard, name='TaskDashboard'),
    path('contest/api/<int:id>/upload_package', views.UploadContestTaskPackage, name='UploadContestTaskPackage'),
]
