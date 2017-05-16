# encoding: utf-8
import django_tables2 as tables
from .models import Contest, Notification, Clarification, ContestSubmission
from django_tables2.utils import A


class ContestTable(tables.Table):
    title = tables.LinkColumn('contest:contest-detail', args=[A('pk')])
    group = tables.LinkColumn('mygroup-detail', args=[A('group.pk')])

    class Meta:
        model = Contest
        fields = ('title', 'author', 'group', 'start_time')
        template = 'django_tables2/bootstrap.html'


class NotificationTable(tables.Table):

    status = tables.TemplateColumn(
        template_name="contest/notification_list_external.html",
        orderable=False,
        verbose_name='Operator',
    )

    class Meta:
        model = Notification
        fields = ('title', 'content', 'create_time', 'status')
        template = 'django_tables2/bootstrap.html'


class ClarificationTable(tables.Table):

    status = tables.TemplateColumn(
        template_name="contest/clarification_list_external.html",
        orderable=False,
        verbose_name='Operator',
    )

    class Meta:
        model = Clarification
        fields = ('author', 'question', 'answer', 'status')
        template = 'django_tables2/bootstrap.html'


class SubmissionTable(tables.Table):
    pk = tables.LinkColumn('contest:submission-detail', args=[A('problem.contest.pk'), A('pk')], verbose_name='id')
    problem = tables.LinkColumn('contest:problem-detail', args=[A('problem.contest.pk'), A('problem.index')])
    status = tables.Column(accessor='submission.status')
    running_time = tables.Column(accessor='submission.running_time')
    running_memory = tables.Column(accessor='submission.running_memory')
    language = tables.Column(accessor='submission.language')
    user = tables.Column(accessor='submission.user')
    create_time = tables.DateColumn(accessor='submission.create_time')

    class Meta:
        model = ContestSubmission
        fields = ('pk', 'problem', 'status', 'running_time', 'running_memory', 'language',
                  'user', 'create_time')
        template = 'django_tables2/bootstrap.html'
