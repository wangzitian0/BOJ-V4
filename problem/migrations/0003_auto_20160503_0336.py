# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0002_auto_20160502_1700'),
    ]

    operations = [
        migrations.RenameField(
            model_name='problem',
            old_name='author',
            new_name='superadmin',
        ),
    ]
