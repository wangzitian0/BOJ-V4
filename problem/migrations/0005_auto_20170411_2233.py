# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0004_auto_20170410_0009'),
    ]

    operations = [
        migrations.AddField(
            model_name='problemcase',
            name='sample_in',
            field=models.CharField(max_length=256, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='problemcase',
            name='sample_out',
            field=models.CharField(max_length=256, null=True, blank=True),
        ),
    ]
