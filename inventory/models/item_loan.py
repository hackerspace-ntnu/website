from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone

from applications.validators import validate_phone_number


def validate_consent(boolean):
    if boolean is not True:
        raise ValidationError("Du må samtykke til at vi kan lagre kontaktinformasjon")


class ItemLoan(models.Model):
    """Contains information about borrowing an item in inventory"""

    item = models.ForeignKey(
        "inventory.itemloan", on_delete=models.CASCADE, verbose_name="Lånegjenstand"
    )
    amount = models.IntegerField("Antall", validators=[MinValueValidator(1)])

    # Automatically set once the application is accepted
    loan_from = models.DateField("Utlånt fra", default=timezone.now, blank=True)
    loan_to = models.DateField("Lån til")
    purpose = models.CharField("Formål", max_length=50)

    # Personal information
    contact_name = models.CharField("Utlåners navn", max_length=100)
    contact_phone = models.CharField(
        "Utlåners tlf.",
        max_length=20,
        validators=[validate_phone_number],
    )
    contact_email = models.EmailField("Utlåners e-post")
    # Simply to store and prove that the user consented to having
    # their personal info stored for the duration of the loan
    consent = models.BooleanField(
        "Datalagringssamtykke", blank=False, validators=[validate_consent]
    )

    approver = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Godkjenner",
    )

    def overdue(self):
        """Checks if the loan is overdue for return"""
        return timezone.now().date() > self.loan_to
