# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0002_auto_20151108_2221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='code_language',
            field=models.CharField(default=b'g++', max_length=8, choices=[(b'gcc', b'GNU C'), (b'g++', b'GNU C++'), (b'java', b'java')]),
        ),
    ]
