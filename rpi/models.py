from django.core.validators import RegexValidator
from django.db import models


class RaspberryPi(models.Model):
    name = models.CharField(max_length=50)
    lastSeen = models.DateTimeField('last seen')
    ip = models.CharField('IP', max_length=15,validators=[RegexValidator(r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$')])
    mac = models.CharField('MAC', max_length=17, default="12:34:56:78:90:ab",validators=[RegexValidator(r'^([a-f0-9]{2}:){5}[a-f0-9]{2}$')])

    def __str__(self):
        return self.name
