# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0007_auto_20170128_2340'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problem',
            name='is_spj',
            field=models.BooleanField(default=False),
        ),
    ]
