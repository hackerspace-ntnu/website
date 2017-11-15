from os.path import join, dirname, realpath

from django.core.validators import RegexValidator
from django.db import models

MAC_VALIDATOR = RegexValidator(r'^([a-f0-9]{2}:){5}[a-f0-9]{2}$')


# PI_NAMES_FILE = join(dirname(realpath(__file__)), 'availnames.txt')


class Name(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
        blank=False,
        null=False,
    )

    def __str__(self):
        return self.name


class RaspberryPi(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
        blank=False,
        null=False,
    )
    last_seen = models.DateTimeField(
        verbose_name='last seen',
        blank=False,
        null=False,
    )
    ip = models.GenericIPAddressField(
        verbose_name='IP',
        blank=False,
        null=False,
    )
    mac = models.CharField(
        verbose_name='MAC',
        max_length=17,
        validators=[MAC_VALIDATOR],
        unique=True,
        db_index=True,
        blank=False,
        null=False,
    )

    def __str__(self):
        return self.name

    @staticmethod
    def suggest_name():
        names = Name.objects.values_list('name', flat=True)
        used_names = RaspberryPi.objects.values_list('name', flat=True)
        available_names = set(names) - set(used_names)
        n = 0
        while not available_names:
            available_names = set(map(lambda name: '{}-{}'.format(name, n), names)) - set(used_names)
            n += 1

        return next(iter(available_names))

    @staticmethod
    def get_names():
        return Name.objects.values_list('name',flat=True)
