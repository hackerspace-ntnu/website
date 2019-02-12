from django.contrib.auth.models import User, AnonymousUser, Permission
from django.test import TestCase, RequestFactory, Client
from django.urls import reverse

from reservations.models import Reservation, Queue
from reservations.views import QueueDetailView


class ReservationsTestCase(TestCase):

    def add_permission(self, codename, user=None):
        user = self.user if not user else user
        permission = Permission.objects.get(codename=codename)
        user.user_permissions.add(permission)

    def setUp(self):
        self.queue_shown = Queue.objects.create(name="TestQueueOpen",
                                                description="Test Description",
                                                published=True)
        self.queue_hidden = Queue.objects.create(name="TestQueueHidden",
                                                 description="Another test description",
                                                 published=False)
        self.user = User.objects.create_user(username="adam", email="adam@eve.com", password="test_pass")
        self.user2 = User.objects.create_user(username="ada", email="", password="bleh")
        self.add_permission("add_queue", self.user)

    def test_get_open_queue_anon(self):
        response = self.client.get("/reservations/queue/1")
        self.assertEqual(response.status_code, 200)

    def test_get_open_queue_user(self):
        self.client.login(username="adam", password="test_pass")
        response = self.client.get("/reservations/queue/1")
        self.assertEqual(response.status_code, 200)

    def test_get_hidden_queue_anon(self):
        self.client.logout()
        url = "/reservations/queue/2"
        response = self.client.get(url)
        self.assertRedirects(response, reverse("auth:login") + "?next=" + url)

    def test_get_hidden_queue_wrong_permission(self):
        self.client.login(username="ada", password="bleh")
        url = "/reservations/queue/2"
        response = self.client.get(url)
        self.assertRedirects(response, reverse("auth:login") + "?next=" + url)

    def test_get_hidden_queue_user(self):
        self.client.login(username="adam", password="test_pass")
        response = self.client.get("/reservations/queue/2")
        self.assertEqual(response.status_code, 200)

    def test_get_nonexisting(self):
        self.client.logout()
        response = self.client.get('/reservations/queue/300')
        self.assertEqual(response.status_code, 404)
