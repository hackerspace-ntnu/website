from django.contrib.auth.models import User
from django.db import models
from django.db.models import CharField, TextField, BooleanField, ForeignKey, DateTimeField


class Queue(models.Model):
    name = CharField(
        max_length=64,
        blank=False,
        unique=True,
        verbose_name='navn'
    )
    description = TextField(
        max_length=512,
        default="",
        verbose_name='beskrivelse'
    )
    internal = BooleanField(
        default=False,
        verbose_name='intern'
    )
    hidden = BooleanField(
        default=False,
    )

    def __str__(self):
        return self.name


class Reservation(models.Model):
    parent_queue = ForeignKey(
        Queue,
        related_name='reservations',
        on_delete=models.CASCADE,
        verbose_name='foreldrekø',
    )
    user = ForeignKey(
        User,
        related_name='reservations',
        on_delete=models.CASCADE
    )
    start = DateTimeField(
        blank=False,
        verbose_name='starttidspunkt'
    )
    end = DateTimeField(
        blank=False,
        verbose_name='sluttidspunkt'
    )

    def __str__(self):
        return f'{self.parent_queue}: {self.start:%b %d - %H:%M}'
