# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('score', models.IntegerField(default=0)),
                ('status', models.CharField(default=b'QUE', max_length=3)),
                ('running_time', models.IntegerField(default=0)),
                ('running_memory', models.IntegerField(default=0)),
                ('info', models.TextField(blank=True)),
                ('code', models.TextField()),
                ('Language', models.ForeignKey(related_name='submissions', to='problem.Language')),
                ('problem', models.ForeignKey(to='problem.Problem')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
