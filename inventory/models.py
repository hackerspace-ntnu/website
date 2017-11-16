from django.contrib.auth.admin import User
from django.db import models
from django.db.models import Sum
from django.utils import timezone
from sorl.thumbnail import ImageField

from datetime import timedelta

from files.models import Image


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    visible = models.BooleanField(default=True)

    # TODO lag restriction så den ikke kan være seg selv
    parent_tag = models.ForeignKey('Tag', null=True, related_name="children_tags")

    def get_visible_items(self):
        return self.item_set.filter(visible=True)

    def __str__(self):
        return str(self.name)


class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    quantity = models.IntegerField(default=1)
    thumbnail = models.ForeignKey(Image, on_delete=models.SET_NULL, blank=True, null=True)

    visible = models.BooleanField(default=True)

    tags = models.ManyToManyField(Tag)

    # Felt for plassering i rommet.
    zone = models.CharField(max_length=50, null=True)
    shelf = models.IntegerField(null=True)
    row = models.IntegerField(null=True)
    column = models.IntegerField(null=True)

    # TODO legge til et felt for å telle popularitet i sidevisninger, kan bruke dette når man søker

    def show_tags(self):
        all_tags = ", ".join(str(tag) for tag in self.tags.all())
        return "{} is tagged with {}".format(self.name, all_tags)

    def quantity_left(self):
        """ Returnerer antall items som ikke er lånt ut. """
        if self.loanitem_set.all():
            sum_lent_out = self.loanitem_set.filter(
                loan__visible=True, loan__date_returned=None).aggregate(Sum('quantity'))['quantity__sum']
            return self.quantity - (0 if sum_lent_out is None else sum_lent_out)
        return self.quantity

    def get_active_loans(self):
        loans = []
        for loan_item in self.loanitem_set.filter(loan__date_returned=None):
            loan = loan_item.loan
            if loan and loan.visible:
                loans.append(loan)
        return loans

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
