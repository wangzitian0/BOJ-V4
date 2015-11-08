# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myuser', '0004_bojuser'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bojuser',
            name='birthdate',
        ),
        migrations.RemoveField(
            model_name='bojuser',
            name='preferred_lang',
        ),
        migrations.AddField(
            model_name='bojuser',
            name='default_lang',
            field=models.CharField(default=b'g++', max_length=10),
        ),
    ]
