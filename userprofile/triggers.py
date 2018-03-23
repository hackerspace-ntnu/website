from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from userprofile.models import Profile


# Save a user profile whenever we create a user
@receiver(post_save, sender=User, dispatch_uid="create_profile_on_user_create")
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, auto_duty=False)
