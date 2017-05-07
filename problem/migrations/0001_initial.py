# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('filer', '0002_auto_20150606_2003'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ojuser', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(default='Untitled', max_length=50)),
                ('time_limit', models.IntegerField(default=1000)),
                ('memory_limit', models.IntegerField(default=65536)),
                ('code_length_limit', models.IntegerField(default=65536)),
                ('problem_desc', models.TextField(default='None')),
                ('is_spj', models.BooleanField(default=False)),
                ('is_checked', models.BooleanField(default=False)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('last_updated_time', models.DateTimeField(auto_now=True)),
                ('groups', models.ManyToManyField(related_name='problems', to='ojuser.GroupProfile', blank=True)),
                ('superadmin', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': (('view_problem', 'Can view problem'),),
            },
        ),
        migrations.CreateModel(
            name='ProblemCase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sample_in', models.CharField(max_length=256, null=True, blank=True)),
                ('sample_out', models.CharField(max_length=256, null=True, blank=True)),
                ('score', models.IntegerField(default=0)),
                ('position', models.IntegerField(default=0)),
                ('info', models.TextField(blank=True)),
                ('input_data', models.OneToOneField(related_name='incase', null=True, blank=True, to='filer.File')),
                ('output_data', models.OneToOneField(related_name='outcase', null=True, blank=True, to='filer.File')),
                ('problem', models.ForeignKey(related_name='cases', to='problem.Problem')),
            ],
        ),
        migrations.CreateModel(
            name='ProblemDataInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data', models.OneToOneField(related_name='datainfo', null=True, blank=True, to='filer.File')),
                ('problem', models.ForeignKey(related_name='datainfo', to='problem.Problem')),
            ],
        ),
    ]
