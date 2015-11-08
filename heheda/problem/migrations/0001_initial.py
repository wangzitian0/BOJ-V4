# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myuser', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('pid', models.AutoField(serialize=False, primary_key=True)),
                ('title', models.CharField(default=b'Untitled', max_length=128)),
                ('running_time', models.IntegerField(default=1000)),
                ('running_memory', models.IntegerField(default=65536)),
                ('codelength', models.IntegerField(default=65536)),
                ('prob_desc', models.TextField(default=b'None', max_length=32768)),
                ('is_spj', models.IntegerField(default=0)),
                ('data_count', models.IntegerField(default=0)),
                ('author', models.ForeignKey(to='myuser.UserProfile')),
            ],
        ),
    ]
