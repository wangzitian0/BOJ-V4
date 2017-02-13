from django.db import models
from django.contrib.auth.models import User
from problem.models import Problem
from ojuser.models import Language
from django.core.urlresolvers import reverse
from contest.models import Contest, ContestProblem
from bojv4.conf import CONST 


class Submission(models.Model):
    user = models.ForeignKey(User)
    problem = models.ForeignKey(Problem)
    datetime = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(default=0)
    status = models.CharField(max_length=3, default="QUE", choices=CONST.STATUS_CODE)
    running_time = models.IntegerField(default=0)
    running_memory = models.IntegerField(default=0)
    info = models.TextField(blank=True)
    code = models.TextField()
    language = models.ForeignKey(Language, related_name='submissions')
    contest = models.ForeignKey(Contest, null=True, related_name='submissions')
    contest_problem = models.ForeignKey(ContestProblem, null=True, \
            related_name='submissions')

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


