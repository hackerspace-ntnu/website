from django import forms

from news.forms import MaterialFileWidget
from .models import Profile


class ProfileSearchForm(forms.Form):
    name = forms.CharField(max_length=200)


class ProfileForm(forms.ModelForm):
    image = forms.FileField(required=False, widget=MaterialFileWidget)

    class Meta:
        model = Profile
        fields = ['image', 'access_card', 'study', 'show_email', 'social_discord', 'social_steam', 'social_battlenet',
                  'social_git', 'allergi_gluten', 'allergi_vegetar', 'allergi_vegan', 'allergi_annet', 'limit_social',
                  'phone_number']
