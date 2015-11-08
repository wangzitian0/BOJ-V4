from django.db import models
from myuser.models import BojUser
from contest.models import Contest

# Create your models here.
class Group(models.Model):
    name = models.CharField(max_length=128)
    students = models.ManyToManyField('myuser.BojUser')

class Tag(models.Model):
    tag = models.CharField(max_length=64)
    belong = models.ForeignKey('Group')

class Manage(models.Model):
    admin = models.ForeignKey('myuser.BojUser')
    Group = models.ForeignKey('Group')
    class Meta:
        permissions = (
            ('manage_student', 'manage_contest','view_contest'),
        )

class GroupContest(models.Model):
    name = models.CharField(max_length=64)
    contest = models.ForeignKey('contest.Contest')
    Group = models.ManyToManyField('Group')