# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0004_auto_20170417_0103'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='length',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='submission',
            name='code',
            field=models.TextField(default=b''),
        ),
    ]
