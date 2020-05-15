import random
import string

from django.db import models


def get_random_key():
    return "".join(random.choice(string.ascii_letters) for i in range(8))


class InvitationToken(models.Model):
    value = models.CharField(default=get_random_key, max_length=24)
    email = models.EmailField(max_length=254)

    sent = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
