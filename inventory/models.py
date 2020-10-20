from django.db import models


class Item(models.Model):
    '''Represents a single item in inventory'''

    name = models.CharField('Navn', max_length=100)
    stock = models.IntegerField('Lagerbeholdning')
    description = models.TextField('Beskrivelse', max_length=200, blank=True)
    image = models.ImageField('Bilde', blank=True)

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
    

