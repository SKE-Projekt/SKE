import os

from django.conf import settings

from . import models


def checkSandboxSubmissionTask(source_code, input_code, author):
    sandboxSubmission = models.SandboxSubmission(author=author)
    sandboxSubmission.save()

    try:
        return_code = genSandboxSubmissionFolder(source_code, input_code, sandboxSubmission.special_id)
        if return_code != 0:
            sandboxSubmission.result = 2
        else:
            sandboxSubmission.result = 3
        sandboxSubmission.save()
    except Exception as e:
        print('ERROR: ', e)
        sandboxSubmission.result = 1
        sandboxSubmission.save()

    return sandboxSubmission.id

def genSandboxSubmissionFolder(source_code, input_code, special_id):
    sandboxSubmissionPath = os.path.join(os.path.join(settings.FILES_DIR, 'SKE_SANDBOX'), str(special_id))
    os.makedirs(sandboxSubmissionPath, exist_ok=True)

    sourceCodePath = os.path.join(sandboxSubmissionPath, 'source.ed')
    with open(sourceCodePath, 'w+', encoding='utf-8') as f:
        f.write(source_code.replace('</br>', '\n'))

    inputCodePath = os.path.join(sandboxSubmissionPath, 'input.in')
    with open(inputCodePath, 'w+', encoding='utf-8') as f:
        f.write(input_code.replace('</br>', '\n'))

    return runSandboxSubmission(sandboxSubmissionPath, sourceCodePath, inputCodePath, special_id)

def runSandboxSubmission(sandboxSubmissionPath, sourceCodePath, inputCodePath, special_id):
    outputCodePath = os.path.join(sandboxSubmissionPath, 'output.out')
    run_command = f'{settings.EDLANG_BINARY} {sourceCodePath} < {inputCodePath} > {outputCodePath}'
    print(run_command)

    return os.system(run_command)
