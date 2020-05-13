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
    submit_form = forms.ExerciseSubmissionForm()
    course = get_object_or_404(models.Course, pk=course_id)
    course_children = models.Course.objects.filter(father_course=course)
    course_exercises = models.CourseExercise.objects.filter(course_id=course)
    return render(request, 'SKE_COURSES/course.html', context={'course': course, 'course_children': course_children, 'exercises': course_exercises, 'exer_form': submit_form})

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

def SubmitExerciseSubmission(request, id):
    form = forms.ExerciseSubmissionForm(request.POST)
    if form.is_valid() and request.user.is_authenticated:
        exer = get_object_or_404(models.CourseExercise, pk=id)
        exer_subm_id = tasks.SubmitExerciseSubmission(form.cleaned_data['code'], exer.id, request.user)
        return HttpResponse(exer_subm_id)
    return HttpResponseBadRequest("ERROR")

def GetExerciseSubmissionResult(request, id):
    exer_subm = get_object_or_404(models.ExerciseSubmission, pk=id)

    if request.user == exer_subm.author or request.user.is_superuser:
        return HttpResponse(exer_subm.result)
    return HttpResponseBadRequest()

def GetStartCodeForExercise(request, id):
    exer = get_object_or_404(models.CourseExercise, pk=id)
    exer_subms = models.ExerciseSubmission.objects.filter(exercise=exer, author=request.user).last()

    if exer_subms != None:
        return HttpResponse(exer_subms.code)
    return HttpResponseBadRequest("NONE")
