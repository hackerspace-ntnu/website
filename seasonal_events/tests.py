from django.apps import apps
from django.test import TestCase, SimpleTestCase
from django.template import Context, Template
from seasonal_events.apps import SeasonalEventsConfig 


class SeasonalEventsConfigTest(TestCase):
    def test_apps(self):
        self.assertEqual(SeasonalEventsConfig.name, 'seasonal_events')
        self.assertEqual(apps.get_app_config('seasonal_events').name, 'seasonal_events')
