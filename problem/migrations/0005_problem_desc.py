# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0004_auto_20170502_2317'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='desc',
            field=models.TextField(default='None'),
        ),
    ]
