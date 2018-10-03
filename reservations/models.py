from django.contrib.auth.models import User
from django.db import models
from django.db.models import CharField, TextField, BooleanField, TimeField, ForeignKey, DateField


class Queue(models.Model):
    name = CharField(max_length=64, blank=False, unique=True)
    description = TextField(max_length=512, default="")

    # Visible for regular users or not
    published = BooleanField(default=False)

    def __str__(self):
        return self.name + "[%s]" % self.reservations.count()


class Reservation(models.Model):
    parent_queue = ForeignKey(Queue, related_name='reservations', on_delete=models.CASCADE)
    user = ForeignKey(User, related_name='reservations', on_delete=models.CASCADE)

    date = DateField(blank=False)
    start_time = TimeField(blank=False)
    end_time = TimeField(blank=False)

    def __str__(self):
        return self.user.username + "[%s.%s.%s]" % self.date.isocalendar()
