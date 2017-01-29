# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='NsqTask',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('topic', models.CharField(max_length=30)),
                ('command', models.TextField(max_length=256)),
                ('status', models.IntegerField(default=0)),
                ('user', models.ForeignKey(related_name='nsq_task', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
