# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20151107_2037'),
        ('myuser', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Userhehe',
            fields=[
                ('account_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='account.Account')),
                ('birthdate', models.DateField()),
            ],
            bases=('account.account',),
        ),
    ]
