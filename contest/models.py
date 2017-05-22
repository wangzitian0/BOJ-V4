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
    contest_type = models.IntegerField(default=0, choices=conf.CONTEST_TYPE.choice())

    def __init__(self, *args, **kwargs):
        super(Contest, self).__init__(*args, **kwargs)
        if self.start_time:
            self._start_time = self.start_time.replace(tzinfo=None)

    def __unicode__(self):
        return self.title

    def key(self):
        return 'contest__' + str(self.pk) + '__' + self.title

    @property
    def lang_limited(self):
        res = []
        for x in conf.LANGUAGE_MASK.choice():
            if x[0] & self.lang_limit:
                res.append(x[0])
        return res

    @lang_limited.setter
    def lang_limited(self, value):
        res = 0
        for x in value:
            res |= int(x)
        self.lang_limit = res

    def get_date_time(self):
        return self._start_time.date(), self._start_time.time()

    def time_left(self):
        now = datetime.now()
        if now < self._start_time:
            return self.length
        if now > self._start_time + timedelta(minutes=self.length):
            return 0
        return int((self._start_time + timedelta(minutes=self.length) -now).total_seconds()/60)

    def time_passed_precent(self):
        now = datetime.now()
        if now < self._start_time:
            return 0
        if now > self._start_time + timedelta(minutes=self.length):
            return 100
        return int(((now - self._start_time).total_seconds())*100/(self.length*60))

    def ended(self):
        now = datetime.now()
        if now < self._start_time:
            return -1
        if now > self._start_time + timedelta(minutes=self.length):
            return 1
        return 0

    def last_notification(self):
        if self.notifications.count() == 0:
            return None
        return self.notifications.last().title


class ContestProblem(models.Model):
    contest = models.ForeignKey(Contest, related_name='problems')
    problem = models.ForeignKey(Problem)
    score = models.IntegerField(default=0)
    index = models.CharField(default='A',max_length=2)
    ac_sub = models.IntegerField(default=0)
    all_sub = models.IntegerField(default=0)
    title = models.CharField(max_length=64, default='')

    def __unicode__(self):
        return self.index + '. ' + self.title


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

    author = models.ForeignKey(User, related_name='clarifications')
    question = models.TextField(default='')
    answer = models.TextField(default='')
    create_time = models.DateTimeField(auto_now_add=True)
    contest = models.ForeignKey(Contest, related_name='clarifications')


