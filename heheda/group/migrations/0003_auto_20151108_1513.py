# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0001_initial'),
        ('group', '0002_auto_20151107_2206'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupContest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('Group', models.ManyToManyField(to='group.Group')),
                ('contest', models.ForeignKey(to='contest.Contest')),
            ],
        ),
        migrations.AlterModelOptions(
            name='manage',
            options={'permissions': (('manage_student', 'manage_contest', 'view_contest'),)},
        ),
    ]
