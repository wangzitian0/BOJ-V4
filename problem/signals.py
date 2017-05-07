from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from guardian.shortcuts import assign_perm
from .models import Problem
#  from django.db.models.signals import post_save, m2m_changed
#  from .models import GroupProfile
#  from django.contrib.auth.models import Group
#  from guardian.shortcuts import assign_perm, remove_perm

def change_perm(func, group, instance):
    if not group:
        return
    ancestors = group.get_ancestors(include_self=False)
    descendants = group.get_descendants(include_self=True)
    print ancestors, descendants
    #  here should use cache,  all of  anc,admin,des
    for ans in ancestors:
        func('ojuser.change_problem', ans.admin_group, instance)
        func('ojuser.change_problem', ans.superadmin, instance)
        func('ojuser.view_problem', ans.admin_group, instance)
        func('ojuser.view_problem', ans.superadmin, instance)
    for des in descendants:
        func('ojuser.view_problem', des.user_group, instance)

'''
@receiver(m2m_changed, sender=Problem.groups.through)
def handle_problem_group_save(sender, instance, action, pk_set, reverse, **kwargs):
    print instance, action, pk_set, reverse
    if action == "post_add" and not reverse:
        change_perm(assign_perm, instance, pk_set)
    elif action == "pre_clear" and not reverse:
        change_perm(remove_perm, instance, pk_set)
'''


@receiver(post_save, sender=Problem)
def handle_problem_save(sender, instance, created, **kwargs):
    if created:
        assign_perm('problem.delete_problem', instance.superadmin, instance)
        assign_perm('problem.change_problem', instance.superadmin, instance)
        assign_perm('problem.view_problem', instance.superadmin, instance)
  
'''
@receiver(pre_save, sender=Problem)
def handle_group_pre_save(sender, instance, *args, **kwargs):
    #  print sender, instance, args, kwargs
    if instance.pk:
        for g in instance.groups.all():
            change_perm(remove_perm, g, instance)
'''
