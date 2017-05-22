# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0008_remove_clarification_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clarification',
            name='author',
            field=models.ForeignKey(related_name='clarifications', to=settings.AUTH_USER_MODEL),
        ),
    ]
