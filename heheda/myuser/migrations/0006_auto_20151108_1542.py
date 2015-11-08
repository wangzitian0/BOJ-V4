# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myuser', '0005_auto_20151108_1534'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bojuser',
            name='nickname',
            field=models.CharField(default=b'hehe', max_length=32),
        ),
    ]
