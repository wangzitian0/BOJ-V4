# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('problem', '0001_initial'),
        ('ojuser', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('start_time', models.DateTimeField()),
                ('length', models.IntegerField(default=300)),
                ('board_stop', models.IntegerField(default=300)),
                ('group', models.ForeignKey(to='ojuser.GroupProfile')),
                ('superadmin', models.ForeignKey(related_name='contests', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ContestProblem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.IntegerField(default=0)),
                ('index', models.CharField(default=b'A', max_length=2)),
                ('ac_sub', models.IntegerField(default=0)),
                ('all_sub', models.IntegerField(default=0)),
                ('contest', models.ForeignKey(related_name='problems', to='contest.Contest')),
                ('problem', models.ForeignKey(to='problem.Problem')),
            ],
        ),
        migrations.CreateModel(
            name='ContestSubmission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('problem', models.ForeignKey(related_name='submissions', to='contest.ContestProblem')),
                ('submission', models.ForeignKey(related_name='contest_submissions', to='submission.Submission')),
            ],
        ),
    ]
