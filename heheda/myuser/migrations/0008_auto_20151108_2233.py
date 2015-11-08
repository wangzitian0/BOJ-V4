# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myuser', '0007_auto_20151108_2035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bojuser',
            name='default_lang',
            field=models.CharField(default=b'g++', max_length=8, choices=[(b'gcc', b'GNU C'), (b'g++', b'GNU C++'), (b'java', b'java')]),
        ),
    ]
