# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ojuser', '0015_auto_20170128_2340'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('start_time', models.DateTimeField()),
                ('group', models.ForeignKey(to='ojuser.GroupProfile')),
                ('superadmin', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
