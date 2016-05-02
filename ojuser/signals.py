from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.db.models.signals import m2m_changed

from django.contrib.auth.models import User, Group

from .models import UserProfile, GroupProfile
from guardian.shortcuts import assign_perm, remove_perm


@receiver(post_save, sender=User)
def handle_user_save(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


"""
@receiver(m2m_changed, sender=GroupProfile.admins.through)
def handle_admins_save(sender, instance, action, pk_set, reverse, **kwargs):
    #  print action, instance, pk_set
    #  instance.save()
    pass
"""


def change_perm(func, instance):
    ancestors = instance.get_ancestors(include_self=True)
    descendants = instance.get_descendants(include_self=True)

    #  print ancestors, descendants
    #  here should use cache,  all of  anc,admin,des

    for ans in ancestors:
        for des in descendants:
            func('ojuser.change_groupprofile', ans.superadmin, des)
            func('ojuser.view_groupprofile', des.superadmin, ans)
            func('ojuser.change_groupprofile', ans.admin_group, des)
            func('ojuser.view_groupprofile', des.admin_group, ans)
            func('ojuser.view_groupprofile', des.user_group, ans)


@receiver(post_save, sender=GroupProfile)
def handle_group_save(sender, instance, created, **kwargs):
    change_perm(assign_perm, instance)
    assign_perm('ojuser.delete_groupprofile', instance.superadmin, instance)


@receiver(pre_save, sender=GroupProfile)
def handle_group_delete(sender, instance, *args, **kwargs):
    #  print sender, instance, args, kwargs
    if instance.pk:
        change_perm(remove_perm, instance)
    else:
        instance.user_group = Group.objects.create(
            name=instance.name + "_user_group",
        )
        instance.admin_group = Group.objects.create(
            name=instance.name + "_admin_group",
        )
