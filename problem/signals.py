from django.dispatch import receiver
from django.db.models.signals import m2m_changed
from django.contrib.auth.models import Group

from guardian.shortcuts import assign_perm, get_users_with_perms

from .models import Problem


@receiver(m2m_changed, sender=Problem.groups.through)
def handle_problem_save(sender, instance, action, pk_set, reverse, **kwargs):
    if action == "post_add" and not reverse:
        groups = Group.objects.filter(pk__in=pk_set)
        assign_perm('change_problem', instance.author, instance)
        assign_perm('delete_problem', instance.author, instance)
        assign_perm('view_problem', instance.author, instance)
        res = set()
        for group in groups:
            des = group.profile.descendants_set()
            grp = Group.objects.filter(profile__in=des)
            res.update(grp)
            res.add(group)
        for group in res:
            assign_perm('view_problem', group, instance)
        res = set()
        for group in groups:
            des = group.profile.ancestors_set()
            res.update(des)
            res.add(group.profile)
        users = set()
        for group_profile in res:
            us = get_users_with_perms(group_profile, attach_perms=True)
            for user in us:
                if 'change_groupprofile' in us[user]:
                    users.add(user)
        for user in users:
            assign_perm('change_problem', user, instance)
