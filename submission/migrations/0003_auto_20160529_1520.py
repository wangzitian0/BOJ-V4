# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0002_auto_20160505_0131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='language',
            field=models.ForeignKey(related_name='submissions', to='ojuser.Language'),
        ),
    ]
