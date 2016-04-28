# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nickname', models.CharField(max_length=30)),
                ('desc', models.TextField(blank=True)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('admins', models.ManyToManyField(related_name='managed_group_profiles', to=settings.AUTH_USER_MODEL)),
                ('group', models.OneToOneField(related_name='profile', to='auth.Group')),
                ('parent', mptt.fields.TreeForeignKey(related_name='children', blank=True, to='ojuser.GroupProfile', null=True)),
                ('superadmin', models.ForeignKey(related_name='established_group_profiles', default=1, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': (('view_groupprofile', 'Can view Group Profile'),),
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nickname', models.CharField(max_length=30)),
                ('gender', models.CharField(max_length=1)),
                ('prefer_lang', models.CharField(max_length=4)),
                ('user', models.OneToOneField(related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
