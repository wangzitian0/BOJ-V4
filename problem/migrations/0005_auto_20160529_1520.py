# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0003_auto_20160529_1520'),
        ('problem', '0004_auto_20160505_0036'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Language',
        ),
        migrations.AlterField(
            model_name='problem',
            name='allowed_lang',
            field=models.ManyToManyField(related_name='problems', to='ojuser.Language'),
        ),
    ]
