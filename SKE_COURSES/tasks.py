import os
import json
import tarfile

import markdown2

from django.conf import settings

from . import models


def UploadCoursePackage(coursePackageFile, author):
    course_path = os.path.join(os.path.join(settings.FILES_DIR, 'SKE_COURSES'))
    package_path = UploadCoursePackageFile(coursePackageFile, course_path)

    courseUpload = models.CourseUpload(author=author, path=package_path, result=0)
    courseUpload.save()

    # GEN COURSE FROM PACKAGE
    UploadCoursePackageCelery(course_path, package_path, courseUpload.id)


def UploadCoursePackageCelery(course_path, package_path, upload_id):
    archive_file_path = package_path
    archive_file_path_no_ext = os.path.splitext(os.path.splitext(archive_file_path)[0])[0]
    course_folder = os.path.join(os.path.dirname(course_path), archive_file_path_no_ext)

    UnpackCoursePackage(archive_file_path, course_path)

    json_path = archive_file_path_no_ext + '.json'
    with open(json_path, 'r+', encoding='utf-8') as f:
        current_json = json.loads(f.read())
    
    courseUpload = models.CourseUpload.objects.get(pk=upload_id)
    GenerateCourseFromJSON(current_json, course_path, courseUpload)

############################### Helper functions

def GenerateCourseFromJSON(course_json, courses_path, courseUpload, father=None, depth=0):
    id = int(course_json['id'])
    path = course_json['path']
    title = course_json['title']

    body_path = os.path.join(os.path.join(courses_path, path), 'tresc.md')
    with open(body_path, 'r+', encoding='utf-8') as f:
        body = f.read()
    
    parser = markdown2.Markdown()
    body_parsed = parser.convert(body)

    if father is None:
        course = models.Course(title=title, ord_id=id, upload=courseUpload, body_md=body, body_html=body_parsed)
    else:
        course = models.Course(title=title, father_course=father, ord_id=id, upload=courseUpload, body_md=body, body_html=body_parsed)
    course.save()

    if "subcourses" in course_json:
        for i, sub_course in enumerate(course_json['subcourses']):
            GenerateCourseFromJSON(sub_course, courses_path, courseUpload, course, depth+1)
    if "exercises" in course_json:
        for exer in course_json['exercises']:
            GenerateExerciseFromJSON(exer, courses_path, course)

def GenerateExerciseFromJSON(current_json, courses_path, course):
    id = int(current_json['id'])
    path = current_json['path']
    title = current_json['title']

    body_path = os.path.join(os.path.join(courses_path, path), 'tresc.md')
    with open(body_path, 'r+', encoding='utf-8') as f:
        body = f.read()
    parser = markdown2.Markdown()
    body_parsed = parser.convert(body)

    start_code_path = os.path.join(os.path.join(courses_path, path), 'start.ed')
    with open(start_code_path, 'r+', encoding='utf-8') as f:
        start_code = f.read()
    
    exercise = models.CourseExercise(title=title, path=path, ord_id=id, course_id=course, start_code=start_code, body_md=body, body_html=body_parsed)
    exercise.save()

def UnpackCoursePackage(archive_file_path, course_path):
    tar = tarfile.open(archive_file_path, 'r')
    tar.extractall(course_path)
    tar.close()

def UploadCoursePackageFile(coursePackageFile, course_path):
    os.makedirs(course_path, exist_ok=True)
    course_package_path = os.path.join(course_path, coursePackageFile.name)
    with open(course_package_path, 'wb+') as d:
        for chunk in coursePackageFile.chunks():
            d.write(chunk)
    return course_package_path
