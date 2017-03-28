# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields
from django.conf import settings


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
                ('name', models.CharField(unique=True, max_length=50)),
                ('nickname', models.CharField(max_length=50)),
                ('desc', models.TextField(blank=True)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('admin_group', models.OneToOneField(related_name='admin_profile', null=True, blank=True, to='auth.Group')),
                ('parent', mptt.fields.TreeForeignKey(related_name='children', blank=True, to='ojuser.GroupProfile', null=True)),
                ('superadmin', models.ForeignKey(related_name='group_profile', to=settings.AUTH_USER_MODEL, null=True)),
                ('user_group', models.OneToOneField(related_name='user_profile', null=True, blank=True, to='auth.Group')),
            ],
            options={
                'permissions': (('view_groupprofile', 'Can view Group Profile'),),
            },
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(unique=True, max_length=6)),
                ('name', models.CharField(max_length=30)),
                ('desc', models.TextField(default='None')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nickname', models.CharField(max_length=30)),
                ('gender', models.CharField(default=b'S', max_length=1, choices=[(b'S', 'Secret'), (b'F', 'Female'), (b'M', 'Male')])),
                ('prefer_lang', models.ForeignKey(related_name='user_profiles', default=1, to='ojuser.Language')),
                ('user', models.OneToOneField(related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
