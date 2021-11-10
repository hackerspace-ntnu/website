from django.test import TestCase
from django.urls import reverse
from .models import Item
from .views import InventoryListView, InventoryListAPIView
import time


class ItemTests(TestCase):
    """Tests for the Item model"""

    def test_in_stock(self):
        """You should be able to check if an item is in stock"""
        item = Item.objects.create(name="Test item", stock=20, description="Test")

        self.assertTrue(item.in_stock())

    def test_out_of_stock(self):
        """You should be able to check that an item is out of stock"""
        item = Item.objects.create(name="Test item", stock=0, description="Test")

        self.assertFalse(item.in_stock())


class InventoryListTests(TestCase):
    """Tests for the list view of inventory items"""

    def make_items(self, amount):
        return [
            Item.objects.create(
                name="Test item {}".format(i), stock=i, description="Test"
            )
            for i in range(amount)
        ]

    def test_in_stock(self):
        """In-stock items should show their stock"""
        self.make_items(InventoryListAPIView.paginate_by)
        response = self.client.get(reverse("inventory-api"))
        for stock in range(1, InventoryListAPIView.paginate_by):
            self.assertContains(response, "{} stk.".format(stock))

    def test_out_of_stock(self):
        """Out-of-stock items should say they are out of stock"""
        self.make_items(2)
        response = self.client.get(reverse("inventory-api"))

        # Should denote that there are none of the first item in stock with "Ingen"
        self.assertContains(response, "Ingen")
