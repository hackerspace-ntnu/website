from django.db import models
from datetime import datetime, timedelta
import uuid
from django.contrib.auth.admin import User

VALID_TIME = 2  # 2 hours


class UserAuthentication(models.Model):
    user = models.ForeignKey(User)
    key = models.UUIDField(default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    def activate(self):
        self.user.is_active = True
        self.user.save()
        self.delete()

    def set_password(self, password):
        self.user.set_password(password)
        self.user.save()
        self.delete()

    def expired(self):
        return not datetime.now() < timedelta(hours=VALID_TIME) + self.created
