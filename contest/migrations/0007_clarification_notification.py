# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contest', '0006_contestproblem_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='Clarification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=128)),
                ('question', models.TextField(default=b'')),
                ('answer', models.TextField(default=b'')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('contest', models.ForeignKey(related_name='clarifications', to='contest.Contest')),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=128)),
                ('content', models.TextField(default=b'')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('contest', models.ForeignKey(related_name='notifications', to='contest.Contest')),
            ],
        ),
    ]
