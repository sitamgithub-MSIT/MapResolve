# Django imports
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

# Local imports
from .models import UserProfile


# Create your signals here.
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """
    Creates a user profile when a new user is created.

    Args:
        sender: The sender of the signal.
        instance: The instance of the User model that was just saved.
        created: A boolean indicating whether the instance was just created.
        **kwargs: Additional keyword arguments.

    Returns:
        None
    """
    if created:
        userprofile = UserProfile.objects.create(user=instance)
