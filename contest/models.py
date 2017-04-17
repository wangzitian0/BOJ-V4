from django.db import models
from django.contrib.auth.models import User
from ojuser.models import GroupProfile
from submission.models import Submission
from problem.models import Problem
from bojv4 import conf

# Create your models here.


class Contest(models.Model):

    author = models.ForeignKey(User, related_name='contests')
    group = models.ForeignKey(GroupProfile, related_name='contests')
    name = models.CharField(max_length=30)
    start_time = models.DateTimeField(null=True, blank=True)
    length = models.IntegerField(default=300)
    board_stop = models.IntegerField(default=300)


class ContestProblem(models.Model):
    contest = models.ForeignKey(Contest, related_name='problems')
    problem = models.ForeignKey(Problem)
    score = models.IntegerField(default=0)
    index = models.CharField(default='A',max_length=2)
    ac_sub = models.IntegerField(default=0)
    all_sub = models.IntegerField(default=0)


class ContestSubmission(models.Model):
    problem = models.ForeignKey(ContestProblem, related_name='submissions')
    submission = models.ForeignKey(Submission, related_name='contest_submissions')


"""
class ContestNotification(models.Model):

    TITLE_MIN_LEN = 1
    TITLE_MAX_LEN = 128

    contest = models.ForeignKey(Contest)
    title = models.CharField(max_length=TITLE_MAX_LEN)
    content = models.TextField()
    time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.title



class Clarification(models.Model):
    Q&A in contest
    author = models.ForeignKey(User)
    question = models.TextField()
    answer = models.TextField()
    time = models.DateTimeField(auto_now_add=True)

"""
