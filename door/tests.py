from django.apps import apps
from django.test import TestCase

from door.apps import DoorConfig


class DoorConfigTest(TestCase):
    def test_apps(self):
        self.assertEqual(DoorConfig.name, "door")
        self.assertEqual(apps.get_app_config("door").name, "door")
