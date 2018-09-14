from django import forms
from .models import Profile
from django.contrib.auth.models import User
from django.forms import modelformset_factory, formset_factory, inlineformset_factory, widgets


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'group', 'access_card', 'study', 'skills', 'duty', 'auto_duty']

class ProfileSearchForm(forms.Form):
   name = forms.CharField(max_length=200)

ProfileFormSet = inlineformset_factory(
        User,
        Profile,
        fields=('image',
            'group',
            'access_card',
            'study',
            'skills',
            'duty',
            'auto_duty'),
        widgets={'image': widgets.FileInput()},
        can_delete=False,
        can_order=False)
print(ProfileFormSet())
