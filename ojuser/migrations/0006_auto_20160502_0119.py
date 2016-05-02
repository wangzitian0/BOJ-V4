# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ojuser', '0005_auto_20160502_0117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupprofile',
            name='admin_group',
            field=models.OneToOneField(related_name='admin_profile', null=True, blank=True, to='auth.Group'),
        ),
        migrations.AlterField(
            model_name='groupprofile',
            name='user_group',
            field=models.OneToOneField(related_name='user_profile', null=True, blank=True, to='auth.Group'),
        ),
    ]
