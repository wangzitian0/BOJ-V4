# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('ojuser', '0002_auto_20160502_0056'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='groupprofile',
            name='admins',
        ),
        migrations.RemoveField(
            model_name='groupprofile',
            name='users',
        ),
        migrations.AddField(
            model_name='groupprofile',
            name='admin_group',
            field=models.OneToOneField(related_name='admin_profile', default=1, to='auth.Group'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='groupprofile',
            name='user_group',
            field=models.OneToOneField(related_name='user_profile', default=1, to='auth.Group'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='groupprofile',
            name='superadmin',
            field=models.ForeignKey(related_name='group_profile', to=settings.AUTH_USER_MODEL),
        ),
    ]
