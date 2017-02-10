# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0008_auto_20170129_1657'),
        ('contest', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContestProblem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('index', models.CharField(default=b'A', max_length=2)),
                ('ac_sub', models.IntegerField(default=0)),
                ('problem', models.ForeignKey(to='problem.Problem')),
            ],
        ),
    ]
