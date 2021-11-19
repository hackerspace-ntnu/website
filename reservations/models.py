from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse

from files.models import Image


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
    difficulty = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=3,
        help_text="Velg et tall mellom 1-5, der 1 er lettest",
    )
    internal = models.BooleanField(
        default=False,
    )
    hidden = models.BooleanField(
        default=False,
    )
    out_of_order = models.BooleanField(
        default=False,
    )

    thumbnail = models.ForeignKey(
        Image, null=True, on_delete=models.CASCADE, blank=True
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("reservations:queue_detail", kwargs={"pk": self.pk})

    def get_difficulty_string(self):
        return "★" * self.difficulty + "☆" * (5 - self.difficulty)


class Reservation(models.Model):
    parent_queue = models.ForeignKey(
        Queue,
        related_name="reservations",
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User, related_name="reservations", on_delete=models.CASCADE
    )
    comment = models.CharField(
        max_length=140,
        null=True,
        blank=True,
    )
    start = models.DateTimeField()
    end = models.DateTimeField()

    def __str__(self):
        return self.parent_queue.name + "(" + self.user.get_full_name() + ")"

    def get_absolute_url(self):
        return reverse("reservations:queue_detail", kwargs={"pk": self.parent_queue.pk})

    class Meta:
        permissions = [
            (
                "view_user_details",
                "Can view full name and phone number on reservation view",
            ),
        ]
