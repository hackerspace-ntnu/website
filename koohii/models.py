from django.db import models
from django.utils import timezone


class CoffeePot(models.Model):
    datetime = models.DateTimeField(blank=True,null=True)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    @staticmethod
    def get_coffee_by_name(name):

        # Creates the object if it does not exist
        try:
            coffee = CoffeePot.objects.get(name=name)
            return coffee
        except CoffeePot.DoesNotExist:
            coffee = CoffeePot.objects.create(name=name, datetime=timezone.now().strftime("%a %b %d %H:%M:%S %Z %Y"))
            return coffee

    class Meta:
        verbose_name_plural = "Coffee Pots"


class OpenData(models.Model):
    opened = models.DateTimeField()

    def __str__(self):
        return str(self.opened)

