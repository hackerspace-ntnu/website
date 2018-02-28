from dal import autocomplete
from django import forms

from .models import Committee, Member


class EditCommittees(forms.ModelForm):
    class Meta:
        model = Member
        fields = [
            'committee',
            'position',
            'user',
        ]
        widgets = {
            'user': autocomplete.ModelSelect2(url='verv:user-autocomplete')
                   }


class EditDescription(forms.ModelForm):
    class Meta:
        model = Committee
        fields = [
            'description',
            'one_liner',
            'image',
        ]
