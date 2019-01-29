from django import forms
from .models import Profile
from django.contrib.auth.models import User
from django.forms import modelformset_factory, formset_factory, inlineformset_factory, widgets

class ProfileSearchForm(forms.Form):
   name = forms.CharField(max_length=200)
