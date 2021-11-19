from django.apps import apps
from django.test import TestCase

from news.apps import NewsConfig


class NewsConfigTest(TestCase):
    def test_apps(self):
        self.assertEqual(NewsConfig.name, "news")
        self.assertEqual(apps.get_app_config("news").name, "news")
