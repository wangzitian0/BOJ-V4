from django.db import models

from django.conf import settings
import account

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    birthdate = models.DateField()