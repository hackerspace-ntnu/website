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
        return reverse('queue_detail', kwargs={'pk': self.pk})


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
    start = models.DateTimeField(
        blank=False,
    )
    end = models.DateTimeField(
        blank=False,
    )

    def __str__(self):
        return f'{self.parent_queue}: {self.start:%b %d - %H:%M}'
