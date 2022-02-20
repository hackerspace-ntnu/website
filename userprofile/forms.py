from datetime import datetime, timedelta

from django import forms

from news.forms import MaterialFileWidget

from .models import Profile


class ProfileSearchForm(forms.Form):
    name = forms.CharField(max_length=200)


class ProfileForm(forms.ModelForm):
    image = forms.FileField(required=False, widget=MaterialFileWidget)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super(ProfileForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        has_recent_or_future_reservations = self.user.reservations.filter(
            end__gt=datetime.now() - timedelta(days=1)
        ).exists()
        if cleaned_data["phone_number"] is None and has_recent_or_future_reservations:
            self.add_error(
                "phone_number",
                "Du kan ikke fjerne telefonnummer med nylig gjennomførte (siste 24 timer), pågående eller fremtidige "
                "reservasjoner",
            )

    class Meta:
        model = Profile
        fields = [
            "image",
            "study",
            "show_email",
            "social_discord",
            "social_steam",
            "social_battlenet",
            "social_git",
            "allergi_gluten",
            "allergi_vegetar",
            "allergi_vegan",
            "allergi_annet",
            "limit_social",
            "phone_number",
        ]
