from django.contrib.auth.models import User
from django.db import models
from django.db.models import BooleanField, CharField, DateField, DateTimeField, ForeignKey, TextField
from django.utils import timezone


class Place(models.Model):
  place = CharField(max_length=255, null=False)
  
  def __str__(self):
    return str(self.place)

class Shelf(models.Model):
  shelf = CharField(max_length=255, null=False)
  place = ForeignKey(Place, null=False, on_delete=models.CASCADE)

  def __str__(self):
    return str(self.place) + ": " + str(self.shelf)


class Loan(models.Model):
    lender = CharField(max_length=63)
    created = DateTimeField(auto_now_add=True)
    description_of_loan = TextField(null=True, blank=True)
    returned = BooleanField(default=False)
    user = ForeignKey(User, on_delete=models.CASCADE, null=False)
    from_date = DateField(default=timezone.now)
    to_date = DateField()

    def __str__(self):
        return "Loan: " + "ID: " + str(self.id) + " " + self.user.username + " " + str(self.from_date)


class Asset(models.Model):
  name = CharField(max_length=255, null=False)
  description = TextField(null=True, blank=True)
  place = ForeignKey(Place, on_delete=models.SET_NULL, null=True, blank=True)
  shelf = ForeignKey(Shelf, on_delete=models.SET_NULL, null=True, blank=True)
  loan = ForeignKey(Loan, on_delete=models.SET_NULL, null=True, blank=True)

  def __str__(self):
    return str(self.name)