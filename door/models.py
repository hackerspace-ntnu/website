from django.db import models
from django.utils import timezone
from datetime import datetime

# Create your models here.


class DoorStatus(models.Model):
    datetime = models.DateTimeField()
    status = models.BooleanField(default=False)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class OpenData(models.Model):
    opened = models.DateTimeField()
    closed = models.DateTimeField()

    def __str__(self):
        return str(self.opened)
