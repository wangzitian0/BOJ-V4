from django.dispatch import receiver
from django.db.models.signals import post_save

from django.contrib.auth.models import User, Group

from .models import UserProfile, GroupProfile


@receiver(post_save, sender=User)
def handle_user_save(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=Group)
def handle_group_save(sender, instance, created, **kwargs):
    if created:
        GroupProfile.objects.create(group=instance)
