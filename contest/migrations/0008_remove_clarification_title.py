# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0007_clarification_notification'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clarification',
            name='title',
        ),
    ]
