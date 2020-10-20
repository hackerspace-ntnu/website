from django.db import models


class Item(models.Model):
    '''Represents a single item in inventory'''

    name = models.CharField('Navn', max_length=100)
    stock = models.IntegerField('Lagerbeholdning')
    description = models.CharField('Beskrivelse', max_length=200)
    image = models.ImageField('Bilde', blank=True)

    def __str__(self):
        return self.name + ' (x' + str(self.stock) + ')'

    def in_stock(self):
        '''Whether or not the item is in stock'''
        return self.stock > 0
    

