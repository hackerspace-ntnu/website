from ckeditor_uploader.fields import RichTextUploadingField
from django.core.validators import MinValueValidator
from django.db import models

from files.models import Image
from inventory.models.item_loan import ItemLoan


class Item(models.Model):
    """Represents a single item in inventory"""

    name = models.CharField("Navn", max_length=50)
    stock = models.IntegerField("Lagerbeholdning", validators=[MinValueValidator(0)])
    unknown_stock = models.BooleanField(
        "Ukjent lagerbeholdning", null=False, blank=False, default=False
    )
    can_loan = models.BooleanField("Kan lånes", null=False, blank=False, default=True)
    description = RichTextUploadingField("Beskrivelse", blank=True)
    thumbnail = models.ForeignKey(
        Image, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Bilde"
    )
    location = models.CharField("Hylleplass", max_length=50, blank=True)
    max_loan_duration = models.PositiveIntegerField(
        "Maks lånevarighet (dager)", blank=True, null=True
    )

    views = models.IntegerField("Detaljsidevisninger", default=0, editable=True)

    def __str__(self):
        return self.name + " (x" + str(self.stock) + ")"

    def in_stock(self):
        """Whether or not the item is in stock"""
        return self.available() > 0 or self.unknown_stock

    def has_location(self):
        "Return True if location is not blank"
        return self.location != ""

    def amount_loaned(self):
        """Returns how many of this item was loaned out"""
        try:
            loans = ItemLoan.objects.filter(item=self.id, approver__isnull=False)
            loaned_amount = [loan.amount for loan in loans]
            return sum(loaned_amount)
        except ItemLoan.DoesNotExist:
            return 0

    def next_loan(self):
        loans_sorted = ItemLoan.objects.filter(item__name=self.name).order_by("loan_to")
        for loan in loans_sorted:
            if not loan.overdue():
                return loan
        return None

    def next_loan_done(self):
        formatted_date = (
            str(self.next_loan().loan_to.day)
            + "."
            + str(self.next_loan().loan_to.month)
            + "."
        )
        return formatted_date

    def next_loan_amount(self):
        return self.next_loan().amount

    def available(self):
        """Returns how many items are realistically available"""
        return self.stock - self.amount_loaned()

    def popularity(self):
        """
        Returns a measure of popularity for this item

        For now, this is just the amount of detail page views the item has gotten
        In the future, this may be expanded to weigh other statistics, such as
        how frequently the item is loaned.
        """
        return self.views

    def save(self, *args, **kwargs):
        self.location = self.location.lower()
        return super(Item, self).save(*args, **kwargs)
