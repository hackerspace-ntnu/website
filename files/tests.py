from django.apps import apps
from django.test import TestCase
from files.apps import FilesConfig


class FilesConfigTest(TestCase):
    def test_apps(self):
        self.assertEqual(FilesConfig.name, 'files')
        self.assertEqual(apps.get_app_config('files').name, 'files')
