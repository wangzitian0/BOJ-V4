# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myuser', '0001_initial'),
        ('group', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Manage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'permissions': (('manage_student', 'manage_contest'),),
            },
        ),
        migrations.RemoveField(
            model_name='group',
            name='users',
        ),
        migrations.AddField(
            model_name='group',
            name='students',
            field=models.ManyToManyField(to='myuser.UserProfile'),
        ),
        migrations.AddField(
            model_name='manage',
            name='Group',
            field=models.ForeignKey(to='group.Group'),
        ),
        migrations.AddField(
            model_name='manage',
            name='admin',
            field=models.ForeignKey(to='myuser.UserProfile'),
        ),
    ]
