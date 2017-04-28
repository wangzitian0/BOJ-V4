# encoding: utf-8
import django_tables2 as tables
from .models import Contest
from django_tables2.utils import A


class ContestTable(tables.Table):
    title = tables.LinkColumn('contest:contest-detail', args=[A('pk')])
    group = tables.LinkColumn('mygroup-detail', args=[A('group.pk')])


    class Meta:
        model = Contest
        fields = ('title', 'author', 'group', 'start_time')
        template = 'django_tables2/bootstrap.html'
