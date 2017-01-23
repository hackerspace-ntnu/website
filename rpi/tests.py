import json

from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils.timezone import now

from rpi.models import RaspberryPi


def json_bytes_to_dict(json_bytes):
    return json.loads(json_bytes.decode('ascii'))


class RPiTestCase(TestCase):
    def test_create(self):
        pi = RaspberryPi(
            last_seen=now(),
            mac='12:34:56:78:90:ab',
            name=RaspberryPi.suggest_name(),
            ip='0.0.0.0',
        )
        pi.full_clean()
        pi.save()

    def test_ipv6_valid(self):
        pi = RaspberryPi(
            last_seen=now(),
            mac='12:34:56:78:90:ab',
            name=RaspberryPi.suggest_name(),
            ip='2001:0db8:0000:0042:0000:8a2e:0370:7334',
        )
        pi.full_clean()
        pi.save()

    def test_invalid_ip(self):
        with self.assertRaises(ValidationError):
            pi = RaspberryPi(
                last_seen=now(),
                mac='12:34:56:78:90:ab',
                name=RaspberryPi.suggest_name(),
                ip='1234.x.y.z',
            )
            pi.full_clean()
            pi.save()

    def test_mac_unique(self):
        pi = RaspberryPi(
            last_seen=now(),
            mac='12:34:56:78:90:ab',
            name=RaspberryPi.suggest_name(),
            ip='0.0.0.0',
        )
        pi.full_clean()
        pi.save()

        with self.assertRaises(ValidationError):
            pi = RaspberryPi(
                last_seen=now(),
                mac='12:34:56:78:90:ab',
                name=RaspberryPi.suggest_name(),
                ip='0.0.0.1',
            )
            pi.full_clean()
            pi.save()

    def test_can_make_many_names(self):
        names = RaspberryPi.get_names()

        for i in range(len(names) * 2):
            pi = RaspberryPi(
                last_seen=now(),
                mac='00:00:00:00:00:{:02x}'.format(i),
                name=RaspberryPi.suggest_name(),
                ip='0:0:0:0:0:0:0:{:x}'.format(i),
            )
            pi.full_clean()
            pi.save()


class RPiAPIViewTestCase(TestCase):
    url = reverse('rpi-api')

    def setUp(self):
        self.existing_pi = RaspberryPi.objects.create(
            last_seen=now(),
            mac='12:34:56:78:90:ab',
            name=RaspberryPi.suggest_name(),
            ip='0.0.0.0',
        )

    def test_get(self):
        response = self.client.get(self.url)
        data = json_bytes_to_dict(response.content)

        self.assertEqual(len(data['pis']), 1)

    def test_post_existing_mac(self):
        response = self.client.post(self.url, data={
            'mac_address': self.existing_pi.mac,
        })
        data = json_bytes_to_dict(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['name'], self.existing_pi.name)
        self.assertEqual(RaspberryPi.objects.count(), 1)

    def test_post_new_mac(self):
        response = self.client.post(self.url, data={
            'mac_address': '00:00:00:00:00:00',
        })
        data = json_bytes_to_dict(response.content)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(RaspberryPi.objects.count(), 2)
