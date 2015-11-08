from django.db import models

# Create your models here.
class Problem(models.Model):
    MAX_LEN_TITLE = 128
    MAX_LEN_DESC = 32768
    MAX_LEN_CODE = 65536
    DEFAULT_RUNNING_MEMORY = 65536
    DEFAULT_RUNNING_TIME = 1000
    title = models.CharField(max_length=MAX_LEN_TITLE, default='Untitled')
    running_time = models.IntegerField(default=DEFAULT_RUNNING_TIME) #time limit in ms
    running_memory = models.IntegerField(default=DEFAULT_RUNNING_MEMORY) #memory limit in kb
    codelength = models.IntegerField(default=MAX_LEN_CODE) #code len limit?
    prob_desc = models.TextField(max_length=MAX_LEN_DESC, default='None')
    is_spj = models.IntegerField(default=0) # 0: no spj; 1: all data spj
    author = models.ForeignKey('myuser.UserProfile')
    data_count = models.IntegerField(default=0) # number of test data

 