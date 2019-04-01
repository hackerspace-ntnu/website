from django.apps import apps
from django.test import TestCase
from .apps import CommitteesConfig


class CommitteesConfigTest(TestCase):
    def test_apps(self):
        self.assertEqual(CommitteesConfig.name, 'committees')
        self.assertEqual(apps.get_app_config('committees').name, 'committees')
