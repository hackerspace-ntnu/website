from django.apps import apps
from django.contrib.auth.models import User, AnonymousUser
from django.test import TestCase
from authentication.apps import AuthenticationConfig

from django.conf import settings



class AuthenticationConfigTest(TestCase):
    def test_apps(self):
        self.assertEqual(AuthenticationConfig.name, 'authentication')
        self.assertEqual(apps.get_app_config('authentication').name, 'authentication')
