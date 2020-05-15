from django.urls import path

from . import views


urlpatterns = [
    path('', views.InformationView, name='InformationView'),
    path('sandbox/', views.SandboxView, name='sandbox'),
    path('sandbox/api/submit/', views.SubmitSandboxSubmissionView, name='sandbox_api_submit'),
    path('sandbox/api/get_result/<int:id>', views.GetSandboxSubmissionResult, name='sandbox_api_get_result'),
    path('sandbox/api/get_output/<int:id>', views.GetSandboxSubmissionOutput, name='sandbox_api_get_output')
]
