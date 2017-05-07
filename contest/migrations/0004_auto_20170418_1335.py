# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0003_auto_20170417_2341'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contest',
            old_name='name',
            new_name='title',
        ),
        migrations.AddField(
            model_name='contest',
            name='contest_type',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='contest',
            name='desc',
            field=models.CharField(default=b'', max_length=10000),
        ),
        migrations.AddField(
            model_name='contest',
            name='lang_limit',
            field=models.IntegerField(default=0),
        ),
    ]
