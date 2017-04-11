from django.db import models
from django.contrib.auth.models import User
from problem.models import Problem
from ojuser.models import Language
from django.core.urlresolvers import reverse
from contest.models import Contest, ContestProblem
from django.db.models.signals import pre_save
from django.dispatch import receiver
from bojv4 import conf
from common.nsq_client import send_to_nsq
import json


class Submission(models.Model):
    user = models.ForeignKey(User)
    problem = models.ForeignKey(Problem)
    datetime = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(default=0)
    status = models.CharField(max_length=3, default="QUE", choices=conf.STATUS_CODE.choice())
    running_time = models.IntegerField(default=0)
    running_memory = models.IntegerField(default=0)
    info = models.TextField(blank=True)
    code = models.TextField()
    language = models.CharField(max_length=10, default='gcc', choices=conf.LANGUAGE.choice())

    def __init__(self, *args, **kwargs):
        super(Submission, self).__init__(*args, **kwargs)
        self._info = None

    def __unicode__(self):
        return str(self.pk)
        #  return "-".join([str(self.pk), str(self.user), str(self.problem), str(self.datetime)])

    def get_absolute_url(self):
        return reverse('submission:submission-detail', kwargs={'pk': self.pk})

    @classmethod
    def firstAcInContest(cls, sub):
        if not (sub.contest and sub.status == 'AC'):
            return False
        if cls.objects.filter(contest=sub.contest, user=sub.user, \
                problem=sub.problem, status='AC').count() == 1:
            return True
        return False

    @classmethod
    def notAcInContest(cls, sub):
        if cls.objects.filter(contest=sub.contest, user=sub.user, \
                problem=sub.problem, status='AC').count() == 0:
            return True
        return False

    def set_info(self, key, value):
        if not self._info:
            self._info = {}
            try:
                self._info = json.loads(self.info)
            except Exception as ex:
                self._info = {}
                print ex
        self._info[key] = value

    def deal_case_result(self, case):
        if case.status == 'AC' and self.cases.count() != self.problem.cases.count():
            return
        self.status = case.status
        for c in self.cases.all():
            self.running_time = max(self.running_time, c.running_time)
            self.running_memory = max(self.running_memory, c.running_memory)
        self.save()

    def judge(self):
        req = {
            'grader': 'custom',
            'submission_id': self.id,
            'problem_id': self.problem.id,
            'source': self.code,
            'language': self.language,
            'time_limit': self.problem.time_limit,
            'memory_limit': self.problem.memory_limit,
            'problem_data': self.problem.get_problem_data()
        }
        self.score = 0
        self.status = 'PD'
        self.save()
        send_to_nsq('judge', json.dumps(req))

    def rejudge(self):
        for c in self.cases.all():
            c.delete()
        self.judge()


class CaseResult(models.Model):
    submission = models.ForeignKey(Submission, related_name='cases')
    running_time = models.IntegerField(default=0)
    running_memory = models.IntegerField(default=0)
    status = models.CharField(max_length=3, default="QUE", choices=conf.STATUS_CODE.choice())
    position = models.IntegerField()
    output = models.CharField(max_length=128, default=0)


@receiver(pre_save, sender=Submission)
def dumps_info_callback(sender, instance, created, **kwargs):
    if instance._info:
        instance.info = json.dumps(instance._info)
