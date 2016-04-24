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


@receiver(post_save, sender=Group)
def handle_group_save(sender, instance, created, **kwargs):
    if created:
        GroupProfile.objects.create(group=instance)


@receiver(m2m_changed, sender=GroupProfile.admins.through)
def handle_admins_save(sender, instance, action, pk_set, reverse, **kwargs):
    #  print action, instance, pk_set
    if action == "post_add" and not reverse:
        admins = User.objects.filter(pk__in=pk_set)
        for admin in admins.all():
            instance.group.user_set.add(admin)
    elif action == "post_clear" and not reverse:
        instance.group.user_set.clear()


def change_perm(func, instance):
    ancestors = instance.get_ancestors(include_self=True)
    admins = set()
    for gp in ancestors:
        admins.update(gp.admins.all())
        admins.add(gp.superadmin)

    descendants = instance.get_descendants(include_self=True)

    print ancestors, descendants

    for admin in admins:
        for des in descendants:
            func('change_groupprofile', admin, des)

    for ans in ancestors:
        for des in descendants:
            func('view_groupprofile', des.group, ans)


@receiver(post_save, sender=GroupProfile)
def handle_group_dag_save(sender, instance, *args, **kwargs):
    change_perm(assign_perm, instance)
    instance.group.user_set.add(instance.superadmin)


@receiver(pre_save, sender=GroupProfile)
def handle_group_dag_delete(sender, instance, *args, **kwargs):
    change_perm(remove_perm, instance)
