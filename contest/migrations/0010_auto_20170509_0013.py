# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0009_auto_20170503_0026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='contest_type',
            field=models.IntegerField(default=0, choices=[(0, b'ICPC'), (1, b'OI')]),
        ),
    ]
