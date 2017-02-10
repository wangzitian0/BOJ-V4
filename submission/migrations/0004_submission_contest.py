# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0001_initial'),
        ('submission', '0003_auto_20160529_1520'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='contest',
            field=models.ForeignKey(related_name='submissions', to='contest.Contest', null=True),
        ),
    ]
