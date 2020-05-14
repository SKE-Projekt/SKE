import os
import json
import tarfile

from django.conf import settings
from django.contrib.auth import get_user_model

from celery import shared_task

from . import models


def UploadContestTaskPackage(package, user, contest):
    contest_path = os.path.join(settings.CONTESTS_DIR, str(contest.special_id))
    contest_task_package_path = SaveContestTaskPackage(package, contest_path)

    IntermidiateTask.apply_async(args=(user.id, contest_task_package_path, contest.id))

@shared_task
def IntermidiateTask(user_id, contest_task_package_path, contest_id):
    try:
        user = get_user_model().objects.get(pk=user_id)
        upload = models.ContestTaskPackageUpload(author=user, path=contest_task_package_path)
        upload.save()

        UploadContestTaskPackageCelery(contest_task_package_path, contest_id, upload.id)
        upload.result = 2
    except Exception as e:
        print('[ERROR] Loading Task Pacakge', e, '[END_ERROR]')
        upload.result = 1
    upload.save()

def UploadContestTaskPackageCelery(contest_task_package_path, contest_id, contest_task_upload_id):
    contest = models.Contest.objects.get(pk=contest_id)
    contest_path = os.path.join(settings.CONTESTS_DIR, str(contest.special_id))

    upload = models.ContestTaskPackageUpload.objects.get(pk=contest_task_upload_id)
    
    # DO THINGS
    contest_task_path = UnpackContestTestPackage(contest_task_package_path, contest_path)

    task = GenerateContestTaskFromPath(contest_task_path, contest, upload)
    GenerateContestTasksTestsFromContestTask(task)
    # DONE THINGS

    upload.result = 2

def GenerateContestTasksTestsFromContestTask(contest_task):
    # TODO
    # DO IT BETETER
    task_tests = [os.path.join(contest_task.path, x) for x in os.listdir(contest_task.path) if os.path.isdir(os.path.join(contest_task.path, x))]
    for task_dir in task_tests:
        ord_id = int(os.path.basename(task_dir)[4:])
        task_test = models.ContestTaskTest(task=contest_task, path=task_dir, ord_id=ord_id)
        task_test.save()

def GenerateContestTaskFromPath(contest_task_path, contest, upload):
    # Body
    body_path = os.path.join(contest_task_path, 'body.html')
    with open(body_path, 'r+', encoding='utf-8') as f:
        body = f.read()
    
    # Config
    config_path = os.path.join(contest_task_path, 'config.json')
    with open(config_path, 'r+', encoding='utf-8') as f:
        config = json.loads(f.read())
    
    title = config['title']
    timelimit = config['timelimit']
    sublimit = config['sublimit']
    points = config['points']
    ord_id = config['ord_id']

    task = models.ContestTask(contest=contest, package=upload, ord_id=ord_id, timelimit=timelimit, sublimit=sublimit, body=body, title=title, path=contest_task_path)
    task.save()

    return task

def UnpackContestTestPackage(contest_task_package_path, contest_path):
    contest_task_path = os.path.splitext(os.path.splitext(contest_task_package_path)[0])[0]
    # contest_task_folder_name = os.path.basename(contest_path)

    tar = tarfile.open(contest_task_package_path, 'r')
    tar.extractall(contest_path)
    tar.close()

    return contest_task_path

# def CreateTaskObjectFromPath()

def SaveContestTaskPackage(package, contest_path):
    os.makedirs(contest_path, exist_ok=True)

    contest_task_path = os.path.join(contest_path, package.name)
    with open(contest_task_path, 'wb+') as d:
        for chunk in package.chunks():
            d.write(chunk)

    return contest_task_path
