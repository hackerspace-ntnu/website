from django.db import models
from django.utils import timezone


class KaffeKanne(models.Model):
    datetime = models.DateTimeField(blank=True, null=True)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    @staticmethod
    def get_coffee_by_name(name):
        # Creates the object if it does not exist
        return KaffeKanne.objects.get_or_create(name=name, defaults={'datetime': timezone.now()})[0]

    class Meta:
        verbose_name_plural = "Kaffekanner"


class KaffeData(models.Model):
    brewed = models.DateTimeField()
    pot = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return "{}: {}".format(str(self.pot), str(self.brewed.strftime("%a %b %d %H:%M")))
