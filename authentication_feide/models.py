from django.db import models
from django.contrib.auth.models import AbstractBaseUser

# Create your models here.

class UserModel(AbstractBaseUser):
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'

    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField()
