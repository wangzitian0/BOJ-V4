# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0002_auto_20170429_0059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problem',
            name='tags',
            field=models.ManyToManyField(related_name='problems', null=True, to='problem.ProblemTag', blank=True),
        ),
    ]
