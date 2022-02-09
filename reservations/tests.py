from django.contrib.auth.models import Permission, User
from django.test import Client, TestCase

from reservations.models import Queue


class ReservationsTestCase(TestCase):
    def add_permission(self, codename, user=None):
        user = self.user if not user else user
        permission = Permission.objects.get(codename=codename)
        user.user_permissions.add(permission)

    def setUp(self):
        self.queue = Queue.objects.create(
            name="TestQueueOpen", description="Test Description", hidden=False
        )
        self.queue_hidden = Queue.objects.create(
            name="TestQueueHidden", description="Another test description", hidden=True
        )
        self.user = User.objects.create_user(username="USER", password="PASSWORD")
        self.user2 = User.objects.create_user(username="USER2", password="PASSWORD")
        self.add_permission("add_queue", self.user)
        self.client = Client.login(
            username=self.user.username, password=self.user.password
        )
