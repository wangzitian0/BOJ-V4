# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ojuser', '0014_auto_20170124_1910'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='prefer_lang',
            field=models.ForeignKey(related_name='user_profiles', default=1, to='ojuser.Language'),
        ),
    ]
