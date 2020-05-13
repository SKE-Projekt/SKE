from django.urls import path

from . import views

urlpatterns = [
    path('', views.ListCourses, name='ListCourses'),
    path('course/<int:course_id>', views.ViewCourse, name='ViewCourse'),
    path('api/upload_package/', views.UploadCoursePackage, name='UploadCoursePackage')
]
