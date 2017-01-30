from django.contrib.auth.admin import User  # TODO dette kan være feil, kanskje heller
# django.contrib.auth.models.User hva er isåfall forskjellen? de peker på samme modell
from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=100)
    visible = models.BooleanField(default=True)

    def __str__(self):
        return str(self.name)


class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    quantity = models.IntegerField(default=1)
    visible = models.BooleanField(default=True)

    tags = models.ManyToManyField(Tag)

    # TODO legge til et felt for å telle popularitet i sidevisninger, kan bruke dette når man søker
    # TODO LEGGE TIL ET FELTER FOR HVOR PÅ HACKERSPACEROMMET TINGEN FAKTISK LIGGER
    # TODO antall lånt ut (må holde styr på antall man har tilgjengelig)??

    def show_tags(self):
        all_tags = ", ".join(str(tag) for tag in self.tags.all())
        return "{} is tagged with {}".format(self.name, all_tags)

    def __str__(self):
        return str("name: " + self.name)


class Loan(models.Model):
    # TODO nødvendig med null=True på alle?
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='loan_set')  # lånetaker
    lender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='lender_set')  # utlåner

    comment = models.CharField(max_length=300)
    visible = models.BooleanField(default=True)

    loan_date = models.DateTimeField('date_lent', null=True)
    return_date = models.DateTimeField('return_date', null=True)
    date_returned = models.DateTimeField('date_returned', null=True)  # innleveringstidspunkt (når den faktisk ble
    # levert tilbake)
