from django.db import models
from django.contrib.auth.models import User
from ojuser.models import GroupProfile
from submission.models import Submission
from problem.models import Problem
from bojv4 import conf
from datetime import datetime, timedelta
# Create your models here.


class Contest(models.Model):

    author = models.ForeignKey(User, related_name='contests')
    group = models.ForeignKey(GroupProfile, related_name='contests')
    title = models.CharField(max_length=30)
    start_time = models.DateTimeField(null=True, blank=True)
    length = models.IntegerField(default=300)
    board_stop = models.IntegerField(default=300)
    desc = models.TextField(default='')
    lang_limit = models.IntegerField(default=0)
    contest_type = models.IntegerField(default=0)

    def time_left(self):
        now = datetime.now()
        if now < self.start_time.replace(tzinfo=None):
            return self.length
        if now > (self.start_time.replace(tzinfo=None) + timedelta(minutes=self.length)):
            print now
            print self.start_time
            print (self.start_time.replace(tzinfo=None)+timedelta(minutes=self.length))
            return 0
        print type(self.start_time)
        return int((self.start_time + timedelta(minutes=self.length) -now).total_seconds()/60)


class ContestProblem(models.Model):
    contest = models.ForeignKey(Contest, related_name='problems')
    problem = models.ForeignKey(Problem)
    score = models.IntegerField(default=0)
    index = models.CharField(default='A',max_length=2)
    ac_sub = models.IntegerField(default=0)
    all_sub = models.IntegerField(default=0)
    title = models.CharField(max_length=64, default='')


class ContestSubmission(models.Model):
    problem = models.ForeignKey(ContestProblem, related_name='submissions')
    submission = models.ForeignKey(Submission, related_name='contest_submissions')


class Notification(models.Model):

    contest = models.ForeignKey(Contest, related_name='notifications')
    title = models.CharField(max_length=128)
    content = models.TextField(default='')
    create_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.title



class Clarification(models.Model):

    title = models.CharField(max_length=128)
    author = models.ForeignKey(User)
    question = models.TextField(default='')
    answer = models.TextField(default='')
    create_time = models.DateTimeField(auto_now_add=True)
    contest = models.ForeignKey(Contest, related_name='clarifications')


