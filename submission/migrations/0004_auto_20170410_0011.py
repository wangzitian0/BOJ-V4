# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0003_auto_20170409_0119'),
    ]

    operations = [
        migrations.RenameField(
            model_name='caseresult',
            old_name='score',
            new_name='running_memory',
        ),
        migrations.AddField(
            model_name='caseresult',
            name='running_time',
            field=models.IntegerField(default=0),
        ),
    ]
