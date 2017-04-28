# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0003_auto_20170415_0052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='language',
            field=models.CharField(default=b'gcc', max_length=10, choices=[(b'CPP03', b'GNU C++'), (b'C', b'GNU C'), (b'JAVA8', b'JAVA 8'), (b'CPP11', b'GNU C++ 11'), (b'CPP14', b'GNU C++ 14'), (b'PY2', b'Python 2.7'), (b'PY3', b'Python 3.5'), (b'NASM', b'Assembly 32bit'), (b'NASM64', b'Assembly 64bit')]),
        ),
    ]
