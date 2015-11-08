from django.db import models
from problem.models import Problem
from myuser.models import UserProfile

# Create your models here.
class Contest(models.Model):
    contest_title = models.CharField(max_length=64)
    contest_description = models.TextField(default='')
    start_time = models.DateTimeField()
    length = models.IntegerField(default=300)  # default is 5 hours
    board_stop = models.IntegerField(default=300)  # default is 5 hours, means board won't stop
    board_type = models.IntegerField(default=0)  # 0 for ACM board, 1 for Scroing board, 2 for submit only(submissions won't be judged and will be
                                                 # set to "AC" directly).
    lang_limit = models.IntegerField(default=0)  # mask


class ContestProblem(models.Model):
    title = models.CharField(default='Untitled',max_length=64)
    problem = models.ForeignKey('problem.Problem')
    contest = models.ForeignKey('Contest')


            
class ContestNotice(models.Model):
    contest = models.ForeignKey('Contest')
    title = models.CharField(max_length=64)
    content = models.TextField(default='RT')
    time = models.DateTimeField()


class ContestClarification(models.Model):
    author = models.ForeignKey('myuser.UserProfile')
    contest = models.ForeignKey('Contest')
    question = models.TextField()
    answer = models.TextField()
