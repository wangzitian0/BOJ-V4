# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='language',
            field=models.CharField(default=b'gcc', max_length=10, choices=[(b'CPP03', b'GNU C++'), (b'C', b'GNU C'), (b'JAVA8', b'JAVA 8'), (b'CPP11', b'GNU C++ 11'), (b'PY2', b'Python 2.7')]),
        ),
        migrations.AlterField(
            model_name='submission',
            name='user',
            field=models.ForeignKey(related_name='submissions', to=settings.AUTH_USER_MODEL),
        ),
    ]
