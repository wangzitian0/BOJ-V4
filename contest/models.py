from django.db import models
from django.contrib.auth.models import User
from ojuser.models import GroupProfile
from problem.models import Problem

# Create your models here.

class Contest(models.Model):

    TITLE_MIN_LEN = 1
    TITLE_MAX_LEN = 128
    #cid = models.AutoField(primary_key=True)
    #superadmin = models.ForeignKey('ojuser.UserProfile')
    #group = models.ForeignKey('ojuser.GroupProfile')
    cid = models.IntegerField()
    group = models.CharField(max_length=TITLE_MAX_LEN)

    description = models.TextField(default="")
    title = models.CharField(max_length=TITLE_MAX_LEN)
    start_time = models.DateTimeField()
    duration = models.IntegerField(default=300) # duration of the contest, default is 300 min = 5 hours
    board_stop = models.IntegerField(default=300) # default is 5 hours, means board won't stop in 5 hours
    contest_type = models.IntegerField(default=0) # 0 for acm, 1 for school's contest, 2 for ...

    def __unicode__(self):
        return self.title


class ContestProblem(models.Model):
    #contest = models.ForeignKey('Contest')
    #problem = models.ForeignKey('problem.Problem')
    cpid = models.IntegerField()
    cp_index = models.CharField(max_length=30)
    cp_totalscore = models.IntegerField(default=100) # total
    cp_scores = models.CharField(max_length=128) #format 30|20|20|20|50|30
    cp_title = models.CharField(max_length=128)

    def __unicode__(self):
        return self.cp_index+'.'+self.cp_title

class ContestNotification(models.Model):
    """
    Problem information in Contest
    """

    TITLE_MIN_LEN = 1
    TITLE_MAX_LEN = 128

    #contest = models.ForeignKey('Contest')
    #cnid = models.AutoField(primary_key=True)
    cnid = models.IntegerField()
    title = models.CharField(max_length=TITLE_MAX_LEN)
    content = models.TextField()
    time = models.DateTimeField()

    def __unicode__(self):
        return self.title

class Clarification(models.Model):
    """
    Q&A in contest
    """
    #author = models.ForeignKey('ojuser.UserProfile')
    #ontest_problem = models.ForeignKey('ContestProblem')
    question = models.TextField()
    answer = models.TextField()

    def __unicode__(self):
        return self.question

class ContestProblemSubmission(models.Model):
    """
    submission of a problem in a contest
    """
    #cpsid = models.AutoField(primary_key=True)
    #contest_problem = models.ForeignKey('contest.ContestProblem')
    #user = models.ForeignKey('ojuser.UserProfile')
    cps_resp = models.IntegerField(default=-1) #-1 for not judge, 0 for WA, 1 for AC, 2 for TLE, 3 fro MLE, 4 for CE
    cps_results = models.IntegerField(default=-1) # a binary number means of the result of each data set, only when cps_resp is 0(WA) or 1(AC)
                                                  # eg: 10 sets of data, 1011011101(binary) means set(0,2,3,4,6,7,9) is right and others
                                                  # is wrong, this time cps_res is 0(WA)
    cps_timecost = models.IntegerField()    #with ms
    cps_memerycost = models.IntegerField()  #with KB
    cps_codelength = models.IntegerField()  #with B
    cps_language = models.IntegerField()    #0 for GNU C++, 1 for GNU C, 2 for JAVA,...
    cps_submittime = models.DateTimeField()
