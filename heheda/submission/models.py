from django.db import models
from problem.models import Problem
# Create your models here.
class Submission( models.Model):
    user = models.ForeignKey('myuser.UserProfile')
    problem = models.ForeignKey('problem.Problem')
    status =  models.CharField(max_length=20)
    score = models.IntegerField(default=0)
    code = models.TextField(default='')
    code_language = models.CharField( max_length=20)
    submit_time = models.DateTimeField( auto_now_add=True) # with the former option, it can be stamped at creation time
    runtime = models.IntegerField(default=0)
    runmemory = models.IntegerField(default=0)