from django.db import models
from django.conf import settings
from heheda.conf import CONST
import account


class BojUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    nickname = models.CharField(max_length=30,default='hehe')
    gender = models.CharField(max_length=6,default='secret')
    default_lang = models.CharField(max_length=CONST.LANGUAGE_LENGTH,choices=CONST.LANGUAGE,default=CONST.LANGUAGE_DEFAULT)
