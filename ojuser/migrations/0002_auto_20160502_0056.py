# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ojuser', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='groupprofile',
            old_name='group',
            new_name='users',
        ),
    ]
