from ckeditor_uploader.fields import RichTextUploadingField
from files.models import Image
from django.db import models
from django.core.validators import MinValueValidator, RegexValidator
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Item(models.Model):
    """Represents a single item in inventory"""

    name = models.CharField('Navn', max_length=50)
    stock = models.IntegerField('Lagerbeholdning', validators=[MinValueValidator(0)])
    description = RichTextUploadingField('Beskrivelse', blank=True)
    thumbnail = models.ForeignKey(Image, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Bilde')
    location = models.CharField('Hylleplass', max_length=50, blank=True)

    views = models.IntegerField('Detaljsidevisninger', default=0, editable=True)

    def __str__(self):
        return self.name + ' (x' + str(self.stock) + ')'

    def in_stock(self):
        """Whether or not the item is in stock"""
        return self.available() > 0

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
        loans = ItemLoan.objects.filter(item__name = self.name)
        loans_sorted = sorted(loans, key = lambda loan: loan.loan_to)
        for loan in loans_sorted:
            if not loan.overdue():
                return loan
        return None

    def next_loan_done(self):
        formatted_date = str(self.next_loan().loan_to.day) + "." + str(self.next_loan().loan_to.month) + "."
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


def validate_consent(boolean):
    if boolean is not True:
        raise ValidationError('Du må samtykke til at vi kan lagre kontaktinformasjon')



class ItemLoan(models.Model):
    """Contains information about borrowing an item in inventory"""

    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name='Lånegjenstand')
    amount = models.IntegerField('Antall', validators=[MinValueValidator(1)])

    # Automatically set once the application is accepted
    loan_from = models.DateField('Utlånt fra', default=timezone.now, blank=True)
    loan_to = models.DateField('Lån til')
    purpose = models.CharField('Formål', max_length=50)

    # Personal information
    contact_name = models.CharField('Utlåners navn', max_length=100)
    contact_phone = models.CharField(
        'Utlåners tlf.',
        max_length=8,
        validators=[RegexValidator('^\d{8}$', message='Skriv inn et gyldig telefonnummer')]
    )
    contact_email = models.EmailField('Utlåners e-post')
    # Simply to store and prove that the user consented to having
    # their personal info stored for the duration of the loan
    consent = models.BooleanField('Datalagringssamtykke', blank=False, validators=[validate_consent])

    approver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Godkjenner')

    def overdue(self):
        """Checks if the loan is overdue for return"""
        return timezone.now().date() > self.loan_to
