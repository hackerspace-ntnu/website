from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase

'''
class ViewTestCase(TestCase):
    def setUp(self):
        """Define the test client and other test variables."""
        self.client = APIClient()
        self.tag_data = {"id": 2, "name": "Test Tag", "item_set": []}

    def test_authorization_is_enforced(self):
        new_client = APIClient()
        res = new_client.get('/inventory/tags/1', format="json")
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

'''
