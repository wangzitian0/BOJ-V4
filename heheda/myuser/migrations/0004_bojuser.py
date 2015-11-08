# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myuser', '0003_auto_20151108_1201'),
    ]

    operations = [
        migrations.CreateModel(
            name='BojUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('birthdate', models.DateField()),
                ('nickname', models.CharField(default=b'hehe', max_length=b'32')),
                ('gender', models.CharField(default=b'secret', max_length=6)),
                ('preferred_lang', models.CharField(default=b'g++', max_length=20)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
