import uuid
from datetime import timedelta
from django.utils import timezone

from django.contrib.auth.admin import User
from django.db import models

# Time the activation is valid in hours
VALID_TIME = 2


class UserAuthentication(models.Model):
    user = models.ForeignKey(User)
    key = models.UUIDField(default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    # Activates the user and deletes the authentication object
    def activate(self):
        self.user.is_active = True
        self.user.save()
        self.delete()

    # Set the password and deletes the authentication object
    def set_password(self, password):
        self.user.set_password(password)
        self.user.save()
        self.delete()

    # Checks if the authentication object is expired
    def expired(self):
        return not timezone.now() < timedelta(hours=VALID_TIME) + self.created
