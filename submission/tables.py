# encoding: utf-8
import django_tables2 as tables
from .models import Submission
from django_tables2.utils import A


class SubmissionTable(tables.Table):
    pk = tables.LinkColumn('submission:submission-detail', args=[A('pk')], verbose_name='id')
    problem = tables.LinkColumn('problem:problem-detail', args=[A('problem.pk')])
    status = tables.Column(verbose_name=u'运行结果')

    class Meta:
        model = Submission
        fields = ('pk', 'problem', 'status', 'running_time', 'running_memory', 'language', 'user',
        'create_time')
        template = 'django_tables2/bootstrap.html'

