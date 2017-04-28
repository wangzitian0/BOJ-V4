from django.db import models
from django.contrib.auth.models import User
from problem.models import Problem
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save
from django.dispatch import receiver
from bojv4 import conf
from common.nsq_client import send_to_nsq
import json
import logging
logger = logging.getLogger('django')


class Submission(models.Model):
    CODE_LENGTH_LIMIT = 65536

    user = models.ForeignKey(User, related_name='submissions')
    problem = models.ForeignKey(Problem, related_name='submissions')
    create_time = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(default=0)
    status = models.CharField(max_length=3, default="QUE", choices=conf.STATUS_CODE.choice())
    running_time = models.IntegerField(default=0)
    running_memory = models.IntegerField(default=0)
    info = models.TextField(blank=True)
    code = models.TextField(default='')
    length = models.IntegerField(default=0)
    language = models.CharField(max_length=10, default='gcc', choices=conf.LANGUAGE.choice())

    def __init__(self, *args, **kwargs):
        super(Submission, self).__init__(*args, **kwargs)
        self._info = None

    def __unicode__(self):
        return str(self.pk)
        #  return "-".join([str(self.pk), str(self.user), str(self.problem), str(self.datetime)])

    def get_absolute_url(self):
        return reverse('submission:submission-detail', kwargs={'pk': self.pk})

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
        logger.warning("start pending judge for submission")
        resp = send_to_nsq('judge', json.dumps(req))
        if resp.get('code', None) == -1:
            self.status = 'SE'
            self.save()
            logger.warning("result of pending judge for submission is False, message is " + resp.get('msg'))
        else:
            logger.warning("result of pending judge for submission is True, " + resp.get('msg'))

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
def dumps_info_callback(sender, instance, **kwargs):
    if instance.pk:
        instance.info = json.dumps({})
    elif hasattr(instance, '_info'):
        instance.info = json.dumps(instance._info)
