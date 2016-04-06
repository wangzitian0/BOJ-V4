from django.contrib import admin
from .models import UserProfile, GroupProfile, Consisting
from guardian.admin import GuardedModelAdmin
#  from django.contrib.auth.admin import GroupAdmin
#  from django.contrib.auth.models import Group


class GroupProfileAdmin(GuardedModelAdmin):
    pass


class UserProfileAdmin(GuardedModelAdmin):
    pass

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(GroupProfile, GroupProfileAdmin)
admin.site.register(Consisting)
