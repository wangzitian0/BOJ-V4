# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='code_language',
            field=models.CharField(max_length=16),
        ),
        migrations.AlterField(
            model_name='submission',
            name='status',
            field=models.CharField(max_length=16),
        ),
    ]
