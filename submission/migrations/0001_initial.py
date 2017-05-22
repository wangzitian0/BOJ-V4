# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CaseResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('running_time', models.IntegerField(default=0)),
                ('running_memory', models.IntegerField(default=0)),
                ('status', models.CharField(default=b'QUE', max_length=3, choices=[(b'PD', b'Pending'), (b'SE', b'System Error'), (b'CL', b'Compiling'), (b'CE', b'Compilation Error'), (b'JD', b'Judging'), (b'AC', b'Accepted'), (b'PE', b'Presentation Error'), (b'WA', b'Wrong Answer'), (b'RE', b'Runtime Error'), (b'TLE', b'Time Limit Exceed'), (b'MLE', b'Memory Limit Exceed'), (b'OLE', b'Output Limit Exceed'), (b'EXT', b'Extended Judge Result'), (b'NUM', b'Judge Score')])),
                ('position', models.IntegerField()),
                ('output', models.CharField(default=0, max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('score', models.IntegerField(default=0)),
                ('status', models.CharField(default=b'QUE', max_length=3, choices=[(b'PD', b'Pending'), (b'SE', b'System Error'), (b'CL', b'Compiling'), (b'CE', b'Compilation Error'), (b'JD', b'Judging'), (b'AC', b'Accepted'), (b'PE', b'Presentation Error'), (b'WA', b'Wrong Answer'), (b'RE', b'Runtime Error'), (b'TLE', b'Time Limit Exceed'), (b'MLE', b'Memory Limit Exceed'), (b'OLE', b'Output Limit Exceed'), (b'EXT', b'Extended Judge Result'), (b'NUM', b'Judge Score')])),
                ('running_time', models.IntegerField(default=0)),
                ('running_memory', models.IntegerField(default=0)),
                ('info', models.TextField(blank=True)),
                ('code', models.TextField()),
                ('language', models.CharField(default=b'gcc', max_length=10, choices=[(b'CPP03', b'GNU C++'), (b'C', b'GNU C'), (b'JAVA8', b'java'), (b'CPP11', b'GNU C++ 11'), (b'PY2', b'Python 2.7')])),
                ('problem', models.ForeignKey(to='problem.Problem')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='caseresult',
            name='submission',
            field=models.ForeignKey(related_name='cases', to='submission.Submission'),
        ),
    ]
