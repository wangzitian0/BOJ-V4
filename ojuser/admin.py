from django.contrib import admin
from .models import UserProfile, GroupProfile
from guardian.admin import GuardedModelAdmin

from mptt.admin import MPTTModelAdmin
#  from django.contrib.auth.admin import GroupAdmin
#  from django.contrib.auth.models import Group


class GroupProfileAdmin(GuardedModelAdmin, MPTTModelAdmin):
    pass


class UserProfileAdmin(GuardedModelAdmin):
    pass

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(GroupProfile, GroupProfileAdmin)
