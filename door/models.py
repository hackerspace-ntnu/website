from django.db import models
from django.utils import timezone


class DoorStatus(models.Model):
    datetime = models.DateTimeField()
    status = models.BooleanField(default=False)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    @staticmethod
    def get_door_by_name(name):

        # Creates the object if it does not exist
        try:
            door = DoorStatus.objects.get(name=name)
            return door
        except DoorStatus.DoesNotExist:
            door = DoorStatus.objects.create(name=name, datetime=timezone.now())
            return door

    class Meta:
        verbose_name_plural = "Door Statuses"


class OpenData(models.Model):
    opened = models.DateTimeField()
    closed = models.DateTimeField()

    def __str__(self):
        return str(self.opened)
