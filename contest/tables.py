# encoding: utf-8
import django_tables2 as tables
from .models import Submission
from django_tables2.utils import A


class ContestTable(tables.Table):
    pk = tables.LinkColumn('submission:submission-detail', args=[A('pk')])
    author = tables.LinkColumn('ojuser:account-profile', args=[A('author.pk')])
    group = tables.LinkColumn('ojuser:mygroup-detail', args=[A('group.pk')])


    class Meta:
        model = Submission
        fields = ('pk', 'problem', 'user', 'group', 'start_time')
        template = 'django_tables2/bootstrap.html'
