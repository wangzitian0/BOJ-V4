from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
import account


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    nickname = models.CharField(max_length=30)
    gender = models.CharField(max_length=1)
    prefer_lang = models.CharField(max_length=4)
