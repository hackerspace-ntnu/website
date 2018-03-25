from django.forms import ModelForm
from .models import Item, Tag, Loan




# TODO fyll form med det man hadde isted, når man gjør feil.

class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'description', 'quantity', 'tags','zone','shelf','row','column','thumbnail']


class TagForm(ModelForm):
    class Meta:
        model = Tag
        fields = ['name','visible','parent_tag']

class LoanForm(ModelForm):
    class Meta:
        model = Loan
        fields = ['borrower','lender','comment','visible','loan_date','return_date','date_returned']
