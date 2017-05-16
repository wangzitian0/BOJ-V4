from __future__ import unicode_literals
# from bojv4.conf import CONST
from bojv4 import conf
from django.db import models
from django.contrib.auth.models import User, Group
from mptt.models import MPTTModel, TreeForeignKey


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    nickname = models.CharField(max_length=30)
    gender = models.CharField(
        max_length=1,
        choices=conf.GENDER.choice(),
        default=conf.GENDER.choice()[0][0],
    )

    def __unicode__(self):
        return self.nickname + " (" + self.user.username + ")"


class GroupProfile(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    nickname = models.CharField(max_length=50)
    desc = models.TextField(blank=True)
    user_group = models.OneToOneField(Group, null=True, blank=True, related_name='user_profile')
    admin_group = models.OneToOneField(Group, null=True, blank=True, related_name='admin_profile')
    superadmin = models.ForeignKey(User, null=True, related_name='group_profile')
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)

    class Meta:
        permissions = (
            ('view_groupprofile', 'Can view Group Profile'),
        )

    def __unicode__(self):
        return self.nickname + " [" + self.name + "]"


