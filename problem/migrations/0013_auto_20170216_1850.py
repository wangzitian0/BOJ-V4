# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('filer', '0002_auto_20150606_2003'),
        ('problem', '0012_problemdatainfo_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProblemCase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.IntegerField(default=0)),
                ('info', models.TextField(blank=True)),
                ('input_data', models.OneToOneField(related_name='incase', null=True, blank=True, to='filer.File')),
                ('output_data', models.OneToOneField(related_name='outcase', null=True, blank=True, to='filer.File')),
                ('problem', models.ForeignKey(related_name='case', to='problem.Problem')),
            ],
        ),
        migrations.RemoveField(
            model_name='problemdatainfo',
            name='info',
        ),
        migrations.RemoveField(
            model_name='problemdatainfo',
            name='score',
        ),
    ]
