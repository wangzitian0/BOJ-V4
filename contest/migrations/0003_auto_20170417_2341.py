# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0002_auto_20170417_2320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='group',
            field=models.ForeignKey(related_name='contests', to='ojuser.GroupProfile'),
        ),
    ]
