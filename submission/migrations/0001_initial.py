# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('problem', '0001_initial'),
        ('ojuser', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('score', models.IntegerField(default=0)),
                ('status', models.CharField(default=b'QUE', max_length=3, choices=[(b'PD', b'Pending'), (b'SE', b'System Error'), (b'CL', b'Compiling'), (b'CE', b'Compilation Error'), (b'JD', b'Judging'), (b'AC', b'Accepted'), (b'PE', b'Presentation Error'), (b'WA', b'Wrong Answer'), (b'RE', b'Runtime Error'), (b'TLE', b'Time Limit Exceed'), (b'MLE', b'Memory Limit Exceed'), (b'OLE', b'Output Limit Exceed'), (b'EXT', b'Extended Judge Result'), (b'NUM', b'Judge Score')])),
                ('running_time', models.IntegerField(default=0)),
                ('running_memory', models.IntegerField(default=0)),
                ('info', models.TextField(blank=True)),
                ('code', models.TextField()),
                ('contest', models.ForeignKey(related_name='submissions', to='contest.Contest', null=True)),
                ('contest_problem', models.ForeignKey(related_name='submissions', to='contest.ContestProblem', null=True)),
                ('language', models.ForeignKey(related_name='submissions', to='ojuser.Language')),
                ('problem', models.ForeignKey(to='problem.Problem')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
