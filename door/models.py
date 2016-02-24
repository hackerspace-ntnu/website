from django.db import models

# Create your models here.


class DoorStatus(models.Model):
    status = models.BooleanField(default=False)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name
