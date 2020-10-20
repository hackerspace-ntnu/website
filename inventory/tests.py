from django.test import TestCase
from .models import Item


class ItemTests(TestCase):
    '''Tests for the Item model'''

    def test_in_stock(self):
        '''Test if you can check if an item is in stock'''
        item = Item.objects.create(
            name='Test item',
            stock=20,
            description='Test'
        )

        self.assertTrue(item.in_stock())

    def test_out_of_stock(self):
        '''Test if you can check that an item is out of stock'''
        item = Item.objects.create(
            name='Test item',
            stock=0,
            description='Test'
        )

        self.assertFalse(item.in_stock())
