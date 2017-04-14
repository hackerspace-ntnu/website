from django.contrib.auth.admin import User
from django.db import models
from django.utils import timezone
from sorl.thumbnail import ImageField

from datetime import timedelta


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    visible = models.BooleanField(default=True)

    # TODO lag restriction så den ikke kan være seg selv
    parent_tag = models.ForeignKey('Tag', null=True, related_name="children_tags")

    def __str__(self):
        return str(self.name)


class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    quantity = models.IntegerField(default=1)
    image = ImageField(upload_to='media/inventory', null=True)
    visible = models.BooleanField(default=True)

    tags = models.ManyToManyField(Tag)

    # Felt for plassering i rommet.
    zone = models.CharField(max_length=50, null=True)
    shelf = models.IntegerField(null=True)
    place = models.IntegerField(null=True)

    # TODO legge til et felt for å telle popularitet i sidevisninger, kan bruke dette når man søker

    def show_tags(self):
        all_tags = ", ".join(str(tag) for tag in self.tags.all())
        return "{} is tagged with {}".format(self.name, all_tags)

    def __str__(self):
        return str("name: " + self.name)


class Loan(models.Model):
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='loan_set')  # lånetaker
    lender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='lender_set')  # utlåner

    comment = models.CharField(max_length=300)
    visible = models.BooleanField(default=True)

    loan_date = models.DateTimeField('date_lent', default=timezone.now)
    return_date = models.DateTimeField('return_date', default=timezone.now)
    date_returned = models.DateTimeField('date_returned', null=True)  # innleveringstidspunkt

    def is_past_return_date(self):
        return self.return_date - timezone.now() < timedelta()


class LoanItem(models.Model):
    item = models.ForeignKey(Item)
    loan = models.ForeignKey(Loan, null=True)
    quantity = models.IntegerField(default=1)  # Antall man har lånt av typen item.
