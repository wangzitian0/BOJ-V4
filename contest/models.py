from django.db import models
from django.contrib.auth.models import User
from ojuser.models import GroupProfile
from problem.models import Problem

# Create your models here.

class Contest(models.Model):

    superadmin = models.ForeignKey(User)
    group = models.ForeignKey(GroupProfile)
    name = models.CharField(max_length=30)
    start_time = models.DateTimeField()

class ContestProblem(models.Model):
    problem = models.ForeignKey(Problem)
    index = models.CharField(default='A',max_length=2)
    ac_sub = models.IntegerField(default=0)


