# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0003_problemcase_position'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problemcase',
            name='problem',
            field=models.ForeignKey(related_name='cases', to='problem.Problem'),
        ),
    ]
