from django.dispatch import receiver
from django.db.models.signals import m2m_changed
from django.contrib.auth.models import Group

from guardian.shortcuts import assign_perm, get_users_with_perms

from .models import Problem


@receiver(m2m_changed, sender=Problem.groups.through)
def handle_problem_save(sender, instance, action, pk_set, reverse, **kwargs):
    if action == "post_add" and not reverse:
        assign_perm('change_problem', instance.author, instance)
        assign_perm('delete_problem', instance.author, instance)
        assign_perm('view_problem', instance.author, instance)
        # auth the author all permssion
        groups = Group.objects.filter(pk__in=pk_set)
        # get all groups
        descendants = set()
        for group in groups:
            descendants.add(group)
            des_group_profiles = group.profile.descendants_set()
            des_groups = Group.objects.filter(profile__in=des_group_profiles)
            descendants.update(des_groups)
        for group in descendants:
            assign_perm('view_problem', group, instance)
        # auth all child group view permssion
        ancestor_profiles = set()
        for group in groups:
            ancestor_profiles.add(group.profile)
            anc_group_profile = group.profile.ancestors_set()
            ancestor_profiles.update(anc_group_profile)
        admins = set()
        for group_profile in ancestor_profiles:
            users_with_perms = get_users_with_perms(group_profile, attach_perms=True)
            for user in users_with_perms:
                if 'change_groupprofile' in users_with_perms[user]:
                    admins.add(user)
        for user in admins:
            assign_perm('change_problem', user, instance)
            assign_perm('delete_problem', user, instance)
        # auth all father group admin edit permssion
