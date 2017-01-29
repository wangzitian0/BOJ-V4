# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0006_auto_20170124_1910'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problem',
            name='superadmin',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
