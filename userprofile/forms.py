from django import forms

from .models import Profile


class ProfileForm(forms.Form):
    study = forms.CharField(label='Studieretning', max_length=100)
    card = forms.CharField(label='Adgangskort', max_length=100)


class ProfileModelForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['study', 'access_card']
