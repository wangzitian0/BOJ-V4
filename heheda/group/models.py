from django.db import models

# Create your models here.
class Group(models.Model):
    name = models.CharField(max_length=128)
    students = models.ManyToManyField('myuser.UserProfile')

class Tag(models.Model):
    tag = models.CharField(max_length=64)
    belong = models.ForeignKey('Group')

class Manage(models.Model):
    admin = models.ForeignKey('myuser.UserProfile')
    Group = models.ForeignKey('Group')
    class Meta:
        permissions = (
            ('manage_student', 'manage_contest'),
        )


        