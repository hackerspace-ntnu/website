from django.db import models
from django.contrib.auth.admin import User


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.name)


class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300)

    tags = models.ManyToManyField(Tag)

    def show_tags(self):
        all_tags = ", ".join([str(tag) for tag in self.tags.all()])
        return str(self.name) + " is tagged with: " + all_tags

    def __str__(self):
        return str("name: " + self.name)


class Loan(models.Model):
    borrower = models.ForeignKey(User)  # lånetaker
    # lender = models.ForeignKey(User)  # utlåner
    comment = models.CharField(max_length=300)

    loan_date = models.DateTimeField('date_lent')
    return_date = models.DateTimeField('return_date')
    date_returned = models.DateTimeField('date_returned')  # innleveringstidspunkt (når den faktisk ble levert tilbake)
