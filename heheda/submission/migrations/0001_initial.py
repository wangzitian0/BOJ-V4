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
            name='Submission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(max_length=20)),
                ('score', models.IntegerField(default=0)),
                ('code', models.TextField(default=b'')),
                ('code_language', models.CharField(max_length=20)),
                ('submit_time', models.DateTimeField(auto_now_add=True)),
                ('runtime', models.IntegerField(default=0)),
                ('runmemory', models.IntegerField(default=0)),
                ('problem', models.ForeignKey(to='problem.Problem')),
                ('user', models.ForeignKey(to='myuser.BojUser')),
            ],
        ),
    ]
