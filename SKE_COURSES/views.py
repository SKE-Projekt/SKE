from django.shortcuts import render, HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponseBadRequest
from django.contrib import messages

from . import forms
from . import tasks
from . import models


def ListCourses(request):
    form = forms.CoursePackageForm()
    courses = models.Course.objects.filter(father_course=None)
    return render(request, 'SKE_COURSES/courses_list.html', context={'form': form, 'courses': courses})

def ViewCourse(request, course_id):
    course = get_object_or_404(models.Course, pk=course_id)
    course_children = models.Course.objects.filter(father_course=course)
    course_exercises = models.CourseExercise.objects.filter(course_id=course)
    return render(request, 'SKE_COURSES/course.html', context={'course': course, 'course_children': course_children, 'exercises': course_exercises})

def UploadCoursePackage(request):
    form = forms.CoursePackageForm(request.POST, request.FILES)
    if request.method == "POST" and form.is_valid() and request.user.is_superuser:
        # return HttpResponse(tasks.uploadCoursePackage(form.cleaned_data['course_package_file'])
        # pri)
        tasks.UploadCoursePackage(request.FILES['course_package_file'], request.user)
        messages.add_message(request, messages.SUCCESS, 'Poprawnie przesłano paczkę', 'is-success')
    else:
        messages.add_message(request, messages.ERROR, 'Nie można przesłać paczki', 'is-danger')
    return redirect('ListCourses')
