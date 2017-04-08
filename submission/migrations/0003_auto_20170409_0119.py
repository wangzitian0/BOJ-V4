# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0002_auto_20170408_1825'),
    ]

    operations = [
        migrations.CreateModel(
            name='CaseResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.IntegerField(default=0)),
                ('status', models.CharField(default=b'QUE', max_length=3, choices=[(b'PD', b'Pending'), (b'SE', b'System Error'), (b'CL', b'Compiling'), (b'CE', b'Compilation Error'), (b'JD', b'Judging'), (b'AC', b'Accepted'), (b'PE', b'Presentation Error'), (b'WA', b'Wrong Answer'), (b'RE', b'Runtime Error'), (b'TLE', b'Time Limit Exceed'), (b'MLE', b'Memory Limit Exceed'), (b'OLE', b'Output Limit Exceed'), (b'EXT', b'Extended Judge Result'), (b'NUM', b'Judge Score')])),
                ('position', models.IntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name='submission',
            name='language',
            field=models.CharField(default=b'gcc', max_length=10, choices=[(b'CPP03', b'GNU C++'), (b'C', b'GNU C'), (b'JAVA8', b'java'), (b'CPP11', b'GNU C++ 11'), (b'PY2', b'Python 2.7')]),
        ),
        migrations.AddField(
            model_name='caseresult',
            name='submission',
            field=models.ForeignKey(related_name='cases', to='submission.Submission'),
        ),
    ]
