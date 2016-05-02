# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problem',
            name='groups',
            field=models.ManyToManyField(related_name='problems', to='ojuser.GroupProfile'),
        ),
    ]
