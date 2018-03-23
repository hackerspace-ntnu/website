from django import forms

from .models import Profile, DutyTime, Skill
from django.contrib.auth.models import User


class ProfileForm(forms.Form):
    pass
#    study = forms.CharField(label='Studieretning', max_length=100)
#    access_card = forms.CharField(label='Adgangskort', max_length=100)
#    image = forms.ImageField(label='Profilbilde')
#
#    duty = forms.ModelMultipleChoiceField(DutyTime.objects.all)
#    skills = forms.ModelMultipleChoiceField(Skill.objects.all)

class ProfileModelFormAdmin(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class NameSearchForm(forms.Form):
   name = forms.CharField(max_length=200)
