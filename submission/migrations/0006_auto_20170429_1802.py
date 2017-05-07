# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0005_auto_20170425_2304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='caseresult',
            name='status',
            field=models.CharField(default=b'QUE', max_length=3, choices=[(b'PD', b'Pending'), (b'SE', b'System Error'), (b'CL', b'Compiling'), (b'CE', b'Compilation Error'), (b'JD', b'Judging'), (b'AC', b'Accepted'), (b'PE', b'Presentation Error'), (b'IR', b'Invalid Return'), (b'WA', b'Wrong Answer'), (b'RE', b'Runtime Error'), (b'TLE', b'Time Limit Exceed'), (b'MLE', b'Memory Limit Exceed'), (b'OLE', b'Output Limit Exceed'), (b'IE', b'Internal Error')]),
        ),
        migrations.AlterField(
            model_name='submission',
            name='status',
            field=models.CharField(default=b'QUE', max_length=3, choices=[(b'PD', b'Pending'), (b'SE', b'System Error'), (b'CL', b'Compiling'), (b'CE', b'Compilation Error'), (b'JD', b'Judging'), (b'AC', b'Accepted'), (b'PE', b'Presentation Error'), (b'IR', b'Invalid Return'), (b'WA', b'Wrong Answer'), (b'RE', b'Runtime Error'), (b'TLE', b'Time Limit Exceed'), (b'MLE', b'Memory Limit Exceed'), (b'OLE', b'Output Limit Exceed'), (b'IE', b'Internal Error')]),
        ),
    ]
