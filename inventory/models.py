from ckeditor_uploader.fields import RichTextUploadingField
from files.models import Image
from django.db import models
from django.core.validators import MinValueValidator


class Item(models.Model):
    '''Represents a single item in inventory'''

    name = models.CharField('Navn', max_length=50)
    stock = models.IntegerField('Lagerbeholdning', validators=[MinValueValidator(0)])
    description = RichTextUploadingField('Beskrivelse', blank=True)
    thumbnail = models.ForeignKey(Image, on_delete=models.SET_NULL, null=True, blank=True)

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
