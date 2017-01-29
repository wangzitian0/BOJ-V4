from __future__ import unicode_literals

from django.contrib.auth.models import User
from filer.models.filemodels import File
from django.core.urlresolvers import reverse
from django.db import models
from ojuser.models import GroupProfile

#  from filer.fields.file import FilerFileField


class Problem(models.Model):
    title = models.CharField(max_length=50, default='Untitled')
    time_limit = models.IntegerField(default=1000)
    memory_limit = models.IntegerField(default=65536)
    code_length_limit = models.IntegerField(default=65536)
    problem_desc = models.TextField(default='None')
    is_spj = models.BooleanField(default=False)
    superadmin = models.ForeignKey(User)
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)
    allowed_lang = models.ManyToManyField('ojuser.Language', related_name='problems')
    groups = models.ManyToManyField(GroupProfile, blank=True, related_name='problems')

    def __unicode__(self):
        return str(self.pk) + " " + str(self.title)

    def get_absolute_url(self):
        return reverse('problem:problem-detail', kwargs={'pk': self.pk})

    class Meta:
        permissions = (
            ('view_problem', 'Can view problem'),
        )


def upload_dir(instance, filename):
    return 'documents/{0}/{1}'.format(instance.problem.pk, str(filename))


class ProblemDataInfo(models.Model):
    problem = models.ForeignKey(Problem, related_name="datainfo")
    score = models.IntegerField(default=0)
    data = models.OneToOneField(File, null=True, blank=True, related_name="datainfo")
    info = models.TextField(blank=True)

    def __unicode__(self):
        return str(self.problem.pk) + " " + str(self.pk)
