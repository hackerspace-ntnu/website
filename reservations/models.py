from django.contrib.auth.models import User
from django.db import models
from django.db.models import CharField, TextField, BooleanField, TimeField, ForeignKey, DateField


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
    # Visible for regular users or not
    published = BooleanField(
        default=False,
        verbose_name='publisert'
    )

    def __str__(self):
        return self.name + "[%s]" % self.reservations.count()

    class Meta:
        verbose_name = "kø"
        verbose_name_plural = "køer"


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
    date = DateField(
        blank=False,
        verbose_name='dato'
    )
    start_time = TimeField(
        blank=False,
        verbose_name='starttidspunkt'
    )
    end_time = TimeField(
        blank=False,
        verbose_name='sluttidspunkt'
    )

    def __str__(self):
        return self.user.username + str(self.date)

    class Meta:
        verbose_name = 'reservasjon'
        verbose_name_plural = 'reservasjoner'
        permissions = (('view_name', 'View name of reservee'),)
