# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0003_auto_20170429_1802'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='problem',
            name='problem_desc',
        ),
        migrations.AlterField(
            model_name='problem',
            name='tags',
            field=models.ManyToManyField(related_name='problems', to='problem.ProblemTag', blank=True),
        ),
    ]
