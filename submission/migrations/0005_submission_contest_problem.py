# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0002_contestproblem'),
        ('submission', '0004_submission_contest'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='contest_problem',
            field=models.ForeignKey(related_name='submissions', to='contest.ContestProblem', null=True),
        ),
    ]
