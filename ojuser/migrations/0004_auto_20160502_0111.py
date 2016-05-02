# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ojuser', '0003_auto_20160502_0103'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupprofile',
            name='name',
            field=models.CharField(default=1, unique=True, max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='groupprofile',
            name='nickname',
            field=models.CharField(max_length=50),
        ),
    ]
