from django.urls import path

from . import views


urlpatterns = [
    path('sandbox/', views.SandboxView, name='sandbox'),
    path('sandbox/api/submit/', views.SubmitSandboxSubmissionView, name='sandbox_api_submit')
]
