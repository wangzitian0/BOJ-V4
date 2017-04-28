# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contest',
            old_name='superadmin',
            new_name='author',
        ),
        migrations.AlterField(
            model_name='contest',
            name='start_time',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
