# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ojuser', '0011_auto_20170121_2003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='prefer_lang',
            field=models.ForeignKey(blank=True, to='ojuser.Language', null=True),
        ),
    ]
