# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ojuser', '0012_auto_20170121_2006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='prefer_lang',
            field=models.ForeignKey(related_name='prefer_lang', to='ojuser.Language', null=True),
        ),
    ]
