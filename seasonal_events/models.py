import datetime

from django.db import models


# Date conflicts can arise
class Season(models.Model):
    name = models.CharField(
        max_length=50, verbose_name="navn", help_text="Jul, Påske etc."
    )
    logo = models.ImageField(
        null=True,
        blank=True,
        upload_to="seasonal_events/logos/",
        help_text="Dersom ingen logo lastes opp brukes standard hackerspace-logo",
    )
    start_date = models.DateTimeField(
        verbose_name="startdato", help_text="Prøv å unngå overlapp mellom datoer"
    )
    end_date = models.DateTimeField(
        verbose_name="sluttdato", help_text="Prøv å unngå overlapp mellom datoer"
    )
    active = models.BooleanField(default=True, verbose_name="aktiv")
    repeating = models.BooleanField(
        default=False, verbose_name="repeterende", help_text="Repeteres hvert år"
    )
    manual_override = models.BooleanField(
        verbose_name="Manuel overskriving", help_text="Tving sesongen til å være aktiv"
    )
    disable_reservations = models.BooleanField(
        verbose_name="Hindre reservasjoner",
        help_text="Skru av mulighet for reservasjoner til ikke-medlemmer når denne sesongen er aktiv.",
    )

    def is_now(self):
        if not self.active:
            return False
        if self.manual_override:
            return True
        if self.repeating:
            return (
                self.start_date.day <= datetime.datetime.now().day <= self.end_date.day
            ) and (
                self.start_date.month
                <= datetime.datetime.now().month
                <= self.end_date.month
            )
        return self.start_date <= datetime.datetime.now() <= self.end_date

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Seasons"
