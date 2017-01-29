from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class NsqTask(models.Model):
 
    topic = models.CharField(max_length=30)
    command = models.TextField(max_length=256)
    user = models.ForeignKey(User, related_name='nsq_task')
    status = models.IntegerField(default=0)

    def __unicode__(self):
        return self.topic + ": " + self.command


