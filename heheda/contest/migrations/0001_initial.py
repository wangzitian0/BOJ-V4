# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myuser', '0007_auto_20151108_2035'),
        ('problem', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('contest_title', models.CharField(max_length=64)),
                ('contest_description', models.TextField(default=b'')),
                ('start_time', models.DateTimeField()),
                ('length', models.IntegerField(default=300)),
                ('board_stop', models.IntegerField(default=300)),
                ('board_type', models.IntegerField(default=0)),
                ('lang_limit', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='ContestClarification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question', models.TextField()),
                ('answer', models.TextField()),
                ('author', models.ForeignKey(to='myuser.BojUser')),
                ('contest', models.ForeignKey(to='contest.Contest')),
            ],
        ),
        migrations.CreateModel(
            name='ContestNotice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=64)),
                ('content', models.TextField(default=b'RT')),
                ('time', models.DateTimeField()),
                ('contest', models.ForeignKey(to='contest.Contest')),
            ],
        ),
        migrations.CreateModel(
            name='ContestProblem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(default=b'Untitled', max_length=64)),
                ('contest', models.ForeignKey(to='contest.Contest')),
                ('problem', models.ForeignKey(to='problem.Problem')),
            ],
        ),
    ]
