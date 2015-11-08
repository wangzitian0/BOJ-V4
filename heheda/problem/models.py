from django.db import models
from myuser.models import BojUser
from .conf import CONF

# Create your models here.
class Problem(models.Model):
    title = models.CharField(max_length=CONF.PROBLEM_TITLE_LENGTH, default='Untitled')
    running_time = models.IntegerField(default=CONF.PROBLEM_DEFAULT_RUNNING_TIME) #time limit in ms
    running_memory = models.IntegerField(default=CONF.PROBLEM_DEFAULT_RUNNING_MEMORY) #memory limit in kb
    codelength = models.IntegerField(default=CONF.PROBLEM_MAX_LEN_CODE) #code len limit?
    prob_desc = models.TextField(max_length=CONF.PROBLEM_MAX_LEN_DESC, default='None')
    is_spj = models.IntegerField(default=0) # 0: no spj; 1: all data spj
    author = models.ForeignKey('myuser.BojUser')
    data_count = models.IntegerField(default=0) # number of test data

 