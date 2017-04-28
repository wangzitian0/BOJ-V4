# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0005_auto_20170418_1335'),
    ]

    operations = [
        migrations.AddField(
            model_name='contestproblem',
            name='title',
            field=models.CharField(default=b'', max_length=64),
        ),
    ]
