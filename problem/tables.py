import django_tables2 as tables
from .models import Problem
from django_tables2.utils import A


class ProblemTable(tables.Table):
    title = tables.LinkColumn('problem:problem-detail', args=[A('pk')])
    status = tables.TemplateColumn(
        template_name='problem/problem_list_external.html',
        orderable=False,
    )

    class Meta:
        model = Problem
        fields = ('title', 'time_limit', 'memory_limit', 'author', 'status',)
        template = 'django_tables2/bootstrap.html'
