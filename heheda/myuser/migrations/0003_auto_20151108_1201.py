# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myuser', '0002_userhehe'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userhehe',
            name='account_ptr',
        ),
        migrations.DeleteModel(
            name='Userhehe',
        ),
    ]
