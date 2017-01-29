# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ojuser', '0010_auto_20160529_2056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='prefer_lang',
            field=models.ForeignKey(default='1', to='ojuser.Language'),
        ),
    ]
