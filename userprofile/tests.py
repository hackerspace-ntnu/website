from django.apps import apps
from django.test import TestCase
from userprofile.apps import UserprofileConfig


class UserprofileConfigTest(TestCase):
    def test_apps(self):
        self.assertEqual(UserprofileConfig.name, "userprofile")
        self.assertEqual(apps.get_app_config("userprofile").name, "userprofile")
