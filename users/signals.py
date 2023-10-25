# Django imports
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

# Local imports
from .models import UserProfile


# Create your signals here.
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        userprofile = UserProfile.objects.create(user=instance)
