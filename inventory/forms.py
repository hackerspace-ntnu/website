from dal import autocomplete
from django import forms
import datetime
from .models import Asset, Loan


class LoanForm(forms.ModelForm):
    asset = forms.ModelChoiceField(
        queryset=Asset.objects.filter(loan=None)
    )
    class Meta:
        model = Loan
        fields = ('lender',
                  'user',
                  'asset',
                  'description_of_loan',
                  'from_date',
                  'to_date',
                  'returned'    )

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.save(commit)
        asset = self['asset'].value()
        if(asset != None):
            assetUpdate = Asset.objects.get(id=asset)
            assetUpdate.__setattr__('loan', instance)
            assetUpdate.save(commit)
        if(self['returned'].value()):
            if(asset != None):
                assetRemove = Asset.objects.get(id=asset)
                instance.description_of_loan = self['description_of_loan'].value() + "\nLånte: " + str(assetRemove)
                assetRemove.__setattr__('loan', None)
                assetRemove.save(commit)
        instance.save(commit)
        return instance

    def __init__(self, *args, **kwargs):
        super(LoanForm, self).__init__(*args, **kwargs)
        if self.instance.id is not None:
            assetAdded = [
                [x.id, str(x)] for x in Asset.objects.filter(loan=self.instance)
            ]
            if len(assetAdded) > 0:
                self.fields['asset'] = forms.ChoiceField(
                    choices=assetAdded)


class AssetForm(forms.ModelForm):
    def clean(self, *args, **kwargs):
        place = self.cleaned_data.get('place', None)
        shelf = self.cleaned_data.get('shelf', None)

        if place and shelf and shelf.place_id != place.id:
            raise forms.ValidationError('Wrong Place for Shelf')

    class Meta:
        model = Asset
        fields = ('__all__')
        widgets = {'shelf': autocomplete.ModelSelect2(
            url='inventory:Asset_Place_Shelf_Link', forward=('place',))}