from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from bojv4.conf import CONST
import account


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    nickname = models.CharField(max_length=30, default='heheda')
    gender = models.CharField(max_length=6, default='secret')
    prefer_lang = models.CharField(max_length=6, choices=CONST.LANGUAGE,
        default=CONST.LANGUAGE[0][0])
