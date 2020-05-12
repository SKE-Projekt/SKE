from . import models


def checkSandboxSubmissionTask(source_code, input_code, author):
    sandboxSubmission = models.SandboxSubmission(author=author)
    sandboxSubmission.save()

    return sandboxSubmission.special_id
