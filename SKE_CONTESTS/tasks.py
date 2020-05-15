import os
import json
import tarfile
from timeit import default_timer as timer

from django.conf import settings
from django.contrib.auth import get_user_model

from celery import shared_task

from . import models


################################### SUBMISSSIONS

def SaveTaskSubmission(code, user, task):
    code = code.replace('\r\n', '\n')
    submission = models.ContestTaskSubmission(task=task, author=user, code=code)

    task_tests = models.ContestTaskTest.objects.filter(task=task)
    ttests =[]
    for ttest in task_tests:
        ttests.append(models.ContestTaskSubmissionTest(submit=submission, test=ttest))
    
    # Save everything
    submission.save()
    for a in ttests:
        a.save()
    # Call celery
    RunSubmission.apply_async(args=[submission.id])

@shared_task
def RunSubmission(submission_id):
    submission = models.ContestTaskSubmission.objects.get(pk=submission_id)
    submission_path = os.path.join(submission.task.path, str(submission.special_id))
    submission_tests = models.ContestTaskSubmissionTest.objects.filter(submit=submission)
    correct = 0

    try:
        source_path = SaveSubmissionCode(submission_path, submission.code)

        submission.score = 0
        for stest in submission_tests:
            return_val = RunSubmissionTest(stest, source_path, submission_path)
            if return_val == 4:
                correct += 1
        for stest in submission_tests:
            if stest.score >= 0:
                submission.score += stest.score
        if correct == len(submission_tests):
            submission.result = 4
        elif correct == 0:
            submission.result = 2
        else:
            submission.result = 3
    except Exception as e:
        print('[ERROR]', e, '[END_SUBMISSION_ERROR]')
        submission.result = 1
        submission.score = -1
    submission.save()

def RunSubmissionTest(stest, source_path, submission_path):
    return_code = EvalSubmissionTest(stest, source_path, submission_path)

    if return_code == 0:
        test_result = 4
    elif return_code == -1:
        test_result = 2
    elif return_code == -2:
        test_result = 3
    else:
        test_result = 1

    stest.result = test_result
    stest.save()

    return test_result

def EvalSubmissionTest(stest, source_path, submission_path):
    input_path = os.path.join(stest.test.path, 'input.in')
    expected_output_path = os.path.join(stest.test.path, 'output.out')    
    output_path = os.path.join(submission_path, str(stest.test.ord_id) + '_output.out')

    run_command = f"timeout --preserve-status {stest.test.task.timelimit + 1}s {settings.EDLANG_BINARY} {source_path} < {input_path} > {output_path}"
    check_command = f"diff -B -Z -E --strip-trailing-cr {expected_output_path} {output_path} > /dev/null"
    start = timer()
    run_return = os.system(run_command)
    end = timer()
    time_spent = end - start
    if time_spent > stest.test.task.timelimit:
        stest.score = 0
        return -1
    if run_return:
        return run_return
    check_return = os.system(check_command)
    if check_return:
        stest.score = 0
        return -2
    stest.score = 1
    return 0

def SaveSubmissionCode(path, code):
    os.makedirs(path, exist_ok=True)
    source_path = os.path.join(path, 'source.ed')
    with open(source_path, 'w+', encoding='utf-8') as f:
        f.write(code)

    return source_path

################################### TASK_PCAKAGES

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
