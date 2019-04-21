import datetime

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Queue(models.Model):
    name = models.CharField(
        max_length=64,
        blank=False,
        unique=True,
    )
    description = models.TextField(
        max_length=512,
        default="",
    )
    internal = models.BooleanField(
        default=False,
    )
    hidden = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('reservations:queue_detail', kwargs={'pk': self.pk})


class Reservation(models.Model):
    parent_queue = models.ForeignKey(
        Queue,
        related_name='reservations',
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User,
        related_name='reservations',
        on_delete=models.CASCADE
    )
    comment = models.CharField(
        max_length=140,
        null=True,
        blank=True,
    )
    start_time = models.TimeField()
    end_time = models.TimeField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f'{self.parent_queue}: {self.start_date:%b %d} {self.start_time:%H:%M} - {self.end_time:%H:%M}'

    def get_absolute_url(self):
        return reverse('reservations:queue_detail', kwargs={'pk': self.parent_queue.pk})

    @property
    def start(self):
        return datetime.datetime.combine(self.start_date, self.start_time)

    @property
    def end(self):
        return datetime.datetime.combine(self.end_date, self.end_time)

    class Meta:
        # This is for admin panel only and takes some time. Consider removing and then sorting
        # only when querying for the admin menu
        # https://docs.djangoproject.com/en/2.2/ref/models/options/#ordering
        ordering = [
            '-start_date'
            '-start_time',
        ]
