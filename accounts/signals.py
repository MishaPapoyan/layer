from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, UserProfile
from games.models import Leaderboard


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create UserProfile and Leaderboard entry when a new user is created"""
    if created:
        UserProfile.objects.get_or_create(user=instance)
        Leaderboard.objects.get_or_create(user=instance)

