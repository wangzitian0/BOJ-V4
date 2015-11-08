# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='manage',
            options={'permissions': (('manage_student', 'manage_student'), ('manage_contest', 'manage_contest'), ('view_contest', 'view_contest'))},
        ),
    ]
