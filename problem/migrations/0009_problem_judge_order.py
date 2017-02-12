# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0008_auto_20170129_1657'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='judge_order',
            field=models.BooleanField(default=0),
        ),
    ]
