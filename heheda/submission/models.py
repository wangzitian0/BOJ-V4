from django.db import models
from problem.models import Problem
from myuser.models import BojUser
from .conf import CONF
from heheda.conf import CONST

# Create your models here.
class Submission( models.Model):
    user = models.ForeignKey('myuser.BojUser')
    problem = models.ForeignKey('problem.Problem')
    status =  models.CharField(max_length=CONF.SUBMISSION_STATUS_LENGTH)
    score = models.IntegerField(default=0)
    code = models.TextField(default='')
    code_language = models.CharField(max_length=CONST.LANGUAGE_LENGTH,choices=CONST.LANGUAGE,default=CONST.LANGUAGE_DEFAULT)
    submit_time = models.DateTimeField(auto_now_add=True) # with the former option, it can be stamped at creation time
    runtime = models.IntegerField(default=0)
    runmemory = models.IntegerField(default=0)
