from django.contrib.auth.admin import User
from django.db import models
from django.utils import timezone
from datetime import timedelta
from files.models import Image


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    visible = models.BooleanField(default=True)
    parent_tag = models.ForeignKey('Tag', null=True, blank=True,
                                   related_name="children_tags", on_delete=models.CASCADE)

    def get_visible_items(self):
        return self.item_set.filter(visible=True)

    def __str__(self):
        return str(self.name)


class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    quantity = models.IntegerField(default=1)
    thumbnail = models.ForeignKey(Image, on_delete=models.SET_NULL,
                                  blank=True, null=True)
    visible = models.BooleanField(default=True)
    tags = models.ManyToManyField(Tag)

    # Felt for plassering i rommet.
    zone = models.CharField(max_length=50, null=True)
    shelf = models.IntegerField(null=True)
    row = models.IntegerField(null=True)
    column = models.IntegerField(null=True)

    def quantity_left(self):
        total_quantity = self.quantity
        current_quantity = 0

        loans = self.loans.all()
        for loan in loans:
            current_quantity += loan.quantity

        return (total_quantity - current_quantity)

    def __str__(self):
        return str("<Item>" + self.name)


class Loan(models.Model):
    borrower = models.CharField(max_length=300, null=True)
    email = models.CharField(max_length=300, null=True)
    phone = models.CharField(max_length=300, null=True)
    lender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                               related_name='lender_set')

    comment = models.CharField(max_length=300)
    visible = models.BooleanField(default=True)
    item = models.ForeignKey('Item', on_delete=models.CASCADE, null=True,
                             related_name="loans")
    # Antall man har lånt av typen item.
    quantity = models.IntegerField(default=1)

    loan_date = models.DateTimeField('date_lent', default=timezone.now)
    return_date = models.DateTimeField('return_date', default=timezone.now)
    date_returned = models.DateTimeField('date_returned', null=True)

    def is_past_return_date(self):
        return self.return_date - timezone.now() < timedelta()
