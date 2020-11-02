from ckeditor_uploader.fields import RichTextUploadingField
from files.models import Image
from django.db import models
from django.core.validators import MinValueValidator, RegexValidator
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Item(models.Model):
    '''Represents a single item in inventory'''

    name = models.CharField('Navn', max_length=50)
    stock = models.IntegerField('Lagerbeholdning', validators=[MinValueValidator(0)])
    description = RichTextUploadingField('Beskrivelse', blank=True)
    thumbnail = models.ForeignKey(Image, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Bilde')

    views = models.IntegerField('Detaljsidevisninger', default=0, editable=True)

    def __str__(self):
        return self.name + ' (x' + str(self.stock) + ')'

    def in_stock(self):
        '''Whether or not the item is in stock'''
        return self.stock > 0

    def popularity(self):
        '''
        Returns a measure of popularity for this item
        
        For now, this is just the amount of detail page views the item has gotten
        In the future, this may be expanded to weigh other statistics, such as
        how frequently the item is loaned.
        '''
        return self.views


def validate_true(boolean):
    if boolean is not True:
        raise ValidationError('{} is not True'.format(boolean))


class ItemLoan(models.Model):
    '''Contains information about borrowing an item in inventory'''

    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name='Lånegjenstand')
    amount = models.IntegerField('Antall', validators=[MinValueValidator(1)])

    # Automatically set once the application is accepted
    loan_from = models.DateField('Utlånt fra', default=timezone.now, blank=True)
    loan_to = models.DateField('Utlånt til')
    purpose = models.CharField('Formål', max_length=50)

    # Personal information
    contact_name = models.CharField('Utlåners navn', max_length=100)
    contact_phone = models.CharField(
        'Utlåners tlf.',
        max_length=8,
        validators=[RegexValidator('^\d{8}$', message='Skriv inn et gyldig telefonnummer')]
    )
    contact_email = models.EmailField('Utlåners epost')
    # Simply to store and prove that the user consented to having
    # their personal info stored for the duration of the loan
    consent = models.BooleanField('Datalagringssamtykke', blank=False, validators=[validate_true])

    approver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Godkjenner')
    returned_date = models.DateField('Tilbakelevert på dato', default=None, null=True, blank=True)

    def overdue(self):
        '''Checks if the loan is overdue for return'''
        return timezone.now().date() > self.loan_to and not self.returned_date

    def returned(self):
        '''Marks the item as returned, closing the application'''
        self.returned_date = timezone.now()
        self.save()
