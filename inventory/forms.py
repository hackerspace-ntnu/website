from django import forms
from django.forms.widgets import CheckboxSelectMultiple
from .models import Tag


class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)


class ItemForm(forms.Form):
    name = forms.CharField(label='Gjenstand', max_length=100)
    descritption = forms.CharField(label='Beskrivelse', max_length=300, strip=True)
    quantity = forms.IntegerField(label='Antall')
    # tag = forms.CharField(label='Tag', max_length=100)
    tags = forms.MultipleChoiceField(
        widget=CheckboxSelectMultiple,
        required=False,
        choices=["sko", "fot", "ball", "Pikk"],
    )

    def is_valid(self):
        super().is_valid()



class TagForm(forms.Form):
    name = forms.CharField(label='navn på taggen', max_length=100, strip=True)


class LoanForm(forms.Form):
    borrower = forms.CharField(label='Lånetaker', max_length=100, strip=True)  # username
    # den som låner ut gis implisitt etter hvem som er innlogget
    comment = forms.CharField(label='Kommentar', max_length=300, strip=True)

    # loan date gis implisitt
    return_date = forms.DateField(label='Returdato')
