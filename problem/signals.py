from django.dispatch import receiver
from django.db.models.signals import m2m_changed
from django.contrib.auth.models import Group

from guardian.shortcuts import assign_perm

from .models import Problem


@receiver(m2m_changed, sender=Problem.groups.through)
def handle_problem_save(sender, instance, action, pk_set, reverse, **kwargs):
    if action == "post_add" and not reverse:
        groups = Group.objects.filter(pk__in=pk_set)
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
            grp = Group.objects.filter(profile__in=des)
            res.update(grp)
            res.add(group)
        for group in res:
            assign_perm('change_problem', group, instance)
