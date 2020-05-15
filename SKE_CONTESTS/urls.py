from django.urls import path

from . import views


urlpatterns = [
    path('', views.ListContests, name='ListContests'),
    path('contest/<int:id>', views.ContestDashboard, name='ContestDashboard'),
    path('contest/task/<int:id>', views.TaskDashboard, name='TaskDashboard'),
    path('contest/task/<int:id>/submit', views.SendContestTaskSubmission, name='SendContestTaskSubmission'),
    path('contest/submission/<int:id>', views.SubmissionDashboard, name='SubmissionDashboard'),
    path('contest/<int:id>/submissions', views.ListSubmissions, name='ListSubmissions'),
    path('contest/api/<int:id>/upload_package', views.UploadContestTaskPackage, name='UploadContestTaskPackage'),
]
