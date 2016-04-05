from __future__ import unicode_literals

from django.contrib.auth.models import User
from filer.models.filemodels import File
from django.core.urlresolvers import reverse
from django.db import models

#  from filer.fields.file import FilerFileField


class Problem(models.Model):
    title = models.CharField(max_length=50, default='Untitled')
    time_limit = models.IntegerField(default=1000)
    memory_limit = models.IntegerField(default=65536)
    code_length_limit = models.IntegerField(default=65536)
    problem_desc = models.TextField(default='None')
    is_spj = models.IntegerField(default=0)
    author = models.ForeignKey(User)
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)
    allowed_lang = models.ManyToManyField('Language', related_name='problems')

    def __unicode__(self):
        return str(self.pk) + " " + str(self.title)

    def get_absolute_url(self):
        return reverse('problem:problem-detail', kwargs={'pk': self.pk})

    class Meta:
        permissions = (
            ('view_problem', 'View Problem'),
        )


class Language(models.Model):
    key = models.CharField(max_length=6, unique=True)
    name = models.CharField(max_length=30)
    desc = models.TextField(default='None')

    def __unicode__(self):
        return str(self.name)


def upload_dir(instance, filename):
    return 'documents/{0}/{1}'.format(instance.problem.pk, str(filename))


class ProblemDataInfo(models.Model):
    problem = models.ForeignKey(Problem, related_name="datainfo")
    score = models.IntegerField(default=0)
    data = models.OneToOneField(File, null=True, blank=True, related_name="datainfo")
    info = models.TextField(blank=True)

    def __unicode__(self):
        return str(self.problem.pk) + " " + str(self.pk)
