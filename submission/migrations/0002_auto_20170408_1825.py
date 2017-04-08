# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='submission',
            name='contest',
        ),
        migrations.RemoveField(
            model_name='submission',
            name='contest_problem',
        ),
        migrations.AlterField(
            model_name='submission',
            name='language',
            field=models.CharField(default=b'gcc', max_length=10, choices=[(b'g++', b'GNU C++'), (b'gcc', b'GNU C'), (b'java', b'java'), (b'g+11', b'GNU C++ 11')]),
        ),
    ]
