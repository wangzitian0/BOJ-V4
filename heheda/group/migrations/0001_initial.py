# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0001_initial'),
        ('myuser', '0007_auto_20151108_2035'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('students', models.ManyToManyField(to='myuser.BojUser')),
            ],
        ),
        migrations.CreateModel(
            name='GroupContest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('Group', models.ManyToManyField(to='group.Group')),
                ('contest', models.ForeignKey(to='contest.Contest')),
            ],
        ),
        migrations.CreateModel(
            name='Manage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Group', models.ForeignKey(to='group.Group')),
                ('admin', models.ForeignKey(to='myuser.BojUser')),
            ],
            options={
                'permissions': (('manage_student', 'manage_contest', 'view_contest'),),
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tag', models.CharField(max_length=64)),
                ('belong', models.ForeignKey(to='group.Group')),
            ],
        ),
    ]
