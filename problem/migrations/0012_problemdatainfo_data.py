# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('filer', '0002_auto_20150606_2003'),
        ('problem', '0011_remove_problemdatainfo_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='problemdatainfo',
            name='data',
            field=models.OneToOneField(related_name='datainfo', null=True, blank=True, to='filer.File'),
        ),
    ]
