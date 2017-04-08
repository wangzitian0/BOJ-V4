from django.db import models
from django.contrib.auth.models import User
from problem.models import Problem
from ojuser.models import Language
from django.core.urlresolvers import reverse
from contest.models import Contest, ContestProblem
from bojv4 import conf
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
        if not self.info or self.info == '':
            info = {}
        else:
            try:
                info = json.loads(self.info)
            except Exception, ex:
                print ex
                return
        info[key] = value
        self.info = json.dumps(info)


class CaseResult(models.Model):
    submission = models.ForeignKey(Submission, related_name='cases')
    score = models.IntegerField(default=0)
    status = models.CharField(max_length=3, default="QUE", choices=conf.STATUS_CODE.choice())
    position = models.IntegerField()

    @classmethod
    def deal_case_result(cls, sub, result):
        position = result.get('position')
        case = cls.objects.filter(submission=sub, position=position).first()
        status = result.get('status')
        if not case:
            case = cls(position=position)
            case.submission = sub
        if result.get('status', None) == 'AC':
            sub.score += sub.problem.get_score(position)
        case.status = status
        case.save()


