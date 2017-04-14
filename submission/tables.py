# encoding: utf-8
import django_tables2 as tables
from .models import Submission
from django_tables2.utils import A


class SubmissionTable(tables.Table):
    pk = tables.LinkColumn('submission:submission-detail', args=[A('pk')])
    problem = tables.LinkColumn('problem:problem-detail', args=[A('problem.pk')])
    status = tables.Column(verbose_name=u'运行结果')
    external = tables.TemplateColumn(
        template_name='submission/submission_list_external.html',
        orderable=False,
    )

    class Meta:
        model = Submission
        fields = ('pk', 'problem', 'status', 'user', 'external',)
        template = 'django_tables2/bootstrap.html'
