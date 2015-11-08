from django.db import models
from django.conf import settings
import account


class BojUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    nickname = models.CharField(max_length=32,default='hehe')
    gender = models.CharField(max_length=6,default='secret')
    default_lang = models.CharField(max_length=10,default='g++')
