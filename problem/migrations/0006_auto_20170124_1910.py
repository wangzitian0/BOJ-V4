# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0005_auto_20160529_1520'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problem',
            name='superadmin',
            field=models.ForeignKey(related_name='problems', to=settings.AUTH_USER_MODEL),
        ),
    ]
