# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0004_auto_20170410_0011'),
    ]

    operations = [
        migrations.AddField(
            model_name='caseresult',
            name='output',
            field=models.CharField(default=0, max_length=128),
        ),
    ]
