# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ojuser', '0013_auto_20170121_2020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='prefer_lang',
            field=models.ForeignKey(related_name='user_profile', to='ojuser.Language', null=True),
        ),
    ]
