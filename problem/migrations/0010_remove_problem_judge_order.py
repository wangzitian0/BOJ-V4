# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0009_problem_judge_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='problem',
            name='judge_order',
        ),
    ]
