from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User, Group
from mptt.models import MPTTModel, TreeForeignKey


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    nickname = models.CharField(max_length=30)
    gender = models.CharField(max_length=1)
    prefer_lang = models.CharField(max_length=4)


class GroupProfile(MPTTModel):
    nickname = models.CharField(max_length=30)
    desc = models.TextField(blank=True)
    group = models.OneToOneField(Group, related_name='profile')
    admins = models.ManyToManyField(User, related_name='managed_group_profiles')
    superadmin = models.ForeignKey(User, default=1, related_name='established_group_profiles')
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)

    class Meta:
        permissions = (
            ('view_groupprofile', 'Can view Group Profile'),
        )

    def __unicode__(self):
        return self.group.__unicode__()
