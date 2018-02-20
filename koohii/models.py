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
            coffee = CoffeePot.objects.create(name=name, datetime=timezone.now())
            return coffee

    class Meta:
        verbose_name_plural = "Coffee Pots"


class CoffeeData(models.Model):
    brewed = models.DateTimeField()
    pot = models.CharField(max_length=20,blank=True,null=True)

    def __str__(self):
        return "{}: {}".format(str(self.pot),str(self.brewed))

