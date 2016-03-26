from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from bojv4.conf import CONST


class Problem(models.Model):
    title = models.CharField(max_length=CONST.PROBLEM_TITLE_LENGTH, default='Untitled')
    running_time = models.IntegerField(default=CONST.PROBLEM_DEFAULT_RUNNING_TIME)
    #time limit in ms
    running_memory = models.IntegerField(default=CONST.PROBLEM_DEFAULT_RUNNING_MEMORY)
    #memory limit in kb
    codelength = models.IntegerField(default=CONST.PROBLEM_MAX_LEN_CODE)
    #code len limit?
    prob_desc = models.TextField(max_length=CONST.PROBLEM_MAX_LEN_DESC, default='None')
    is_spj = models.IntegerField(default=0)
    # 0: no spj; 1: all data spj
    author = models.ForeignKey(User)
    data_count = models.IntegerField(default=0)
    # number of test data
