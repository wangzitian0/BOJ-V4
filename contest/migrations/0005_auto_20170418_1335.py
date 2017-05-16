# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0004_auto_20170418_1335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='desc',
            field=models.TextField(default=b''),
        ),
    ]
