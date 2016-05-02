# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('ojuser', '0006_auto_20160502_0119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupprofile',
            name='superadmin',
            field=models.ForeignKey(related_name='group_profile', to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
