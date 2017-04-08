# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0002_remove_problem_allowed_lang'),
    ]

    operations = [
        migrations.AddField(
            model_name='problemcase',
            name='position',
            field=models.IntegerField(default=0),
        ),
    ]
