# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('filer', '0002_auto_20150606_2003'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(unique=True, max_length=6)),
                ('name', models.CharField(max_length=30)),
                ('desc', models.TextField(default='None')),
            ],
        ),
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(default='Untitled', max_length=50)),
                ('time_limit', models.IntegerField(default=1000)),
                ('memory_limit', models.IntegerField(default=65536)),
                ('code_length_limit', models.IntegerField(default=65536)),
                ('problem_desc', models.TextField(default='None')),
                ('is_spj', models.IntegerField(default=0)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('last_updated_time', models.DateTimeField(auto_now=True)),
                ('allowed_lang', models.ManyToManyField(related_name='problems', to='problem.Language')),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('groups', models.ManyToManyField(related_name='problems', to='auth.Group')),
            ],
            options={
                'permissions': (('view_problem', 'Can view problem'),),
            },
        ),
        migrations.CreateModel(
            name='ProblemDataInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.IntegerField(default=0)),
                ('info', models.TextField(blank=True)),
                ('data', models.OneToOneField(related_name='datainfo', null=True, blank=True, to='filer.File')),
                ('problem', models.ForeignKey(related_name='datainfo', to='problem.Problem')),
            ],
        ),
    ]
