from django import forms
from django.contrib.auth.models import User

from .models import TimeTableSlotSignup


class TimeTableSignupForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all(), required=False)

    class Meta:
        model = TimeTableSlotSignup

        fields = (
            "user",
        )

    def clean(self):
        cleaned_data = super().clean()
        if "user" not in cleaned_data.keys():
            cleaned_data["user"] = None
            self.errors.clear()
        return cleaned_data
