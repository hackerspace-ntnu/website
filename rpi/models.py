from os.path import join, dirname, realpath

from django.core.validators import RegexValidator, validate_ipv46_address
from django.db import models

MAC_VALIDATOR = RegexValidator(r'^([a-f0-9]{2}:){5}[a-f0-9]{2}$')
IP_VALIDATOR = validate_ipv46_address
PI_NAMES_FILE = join(dirname(realpath(__file__)), 'availnames.txt')


class RaspberryPi(models.Model):
    name = models.CharField(max_length=50, unique=True, blank=False)
    last_seen = models.DateTimeField('last seen', blank=False)
    ip = models.CharField('IP', max_length=15, validators=[IP_VALIDATOR], blank=False)
    mac = models.CharField('MAC', max_length=17, default='12:34:56:78:90:ab', validators=[MAC_VALIDATOR], unique=True,
                           db_index=True, blank=False)

    def __str__(self):
        return self.name

    @staticmethod
    def get_names():
        with open(PI_NAMES_FILE, mode='r') as f:
            return [name.strip() for name in f.readlines()]

    @staticmethod
    def suggest_name():
        names = RaspberryPi.get_names()
        used_names = RaspberryPi.object.values_list('name', flat=True)
        available_names = set(names) - set(used_names)
        n = 0
        while not available_names:
            available_names = set(map(lambda name: '{}-{}'.format(name, n), names)) - set(used_names)
            n += 1

        return next(iter(available_names))
