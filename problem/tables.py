import django_tables2 as tables
from .models import Problem
from django_tables2.utils import A


class ProblemTable(tables.Table):
    title = tables.LinkColumn('problem:problem-detail', args=[A('pk')])
    status = tables.TemplateColumn(
        """
<p>gg</p>
        """,
        orderable=False,
    )

    class Meta:
        model = Problem
        fields = ('title', 'time_limit', 'memory_limit', 'author', 'status',)
        template = 'django_tables2/bootstrap.html'
