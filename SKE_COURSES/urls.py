from django.urls import path

from . import views

urlpatterns = [
    path('', views.ListCourses, name='ListCourses'),
    path('course/<int:course_id>', views.ViewCourse, name='ViewCourse'),
    path('api/upload_package/', views.UploadCoursePackage, name='UploadCoursePackage'),
    path('api/solve_exercise/<int:id>', views.SubmitExerciseSubmission, name='SubmitExerciseSubmission'),
    path('api/check_solve/<int:id>', views.GetExerciseSubmissionResult, name='GetExerciseSubmissionResult'),
    path('api/get_start_code/<int:id>', views.GetStartCodeForExercise, name='GetStartCodeForExercise'),
]
