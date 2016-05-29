# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ojuser', '0009_auto_20160529_1526'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(default=b'S', max_length=1, choices=[(b'S', 'Secret'), (b'F', 'Female'), (b'M', 'Male')]),
        ),
    ]
