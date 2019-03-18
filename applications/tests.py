from django.apps import apps
from django.test import TestCase
from applications.apps import ApplicationsConfig


class ApplicationsConfigTest(TestCase):
    def test_apps(self):
        self.assertEqual(ApplicationsConfig.name, 'applications')
        self.assertEqual(apps.get_app_config('applications').name, 'applications')
