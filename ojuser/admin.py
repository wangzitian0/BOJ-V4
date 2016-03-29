from django.contrib import admin
from .models import UserProfile, GroupProfile, Consisting

admin.site.register(UserProfile)
admin.site.register(GroupProfile)
admin.site.register(Consisting)
