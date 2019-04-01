import datetime
from django import forms
from django.contrib.auth.models import User

from .models import TimeTableSlotSignup, TimeTable


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


class TimeTableCreationForm(forms.Form):
    year = forms.IntegerField(initial=datetime.datetime.now().year, label="År")
    start_time = forms.TimeField(initial=datetime.time(10, 7), label="Start tid første vakt")
    number_of_slots = forms.IntegerField(min_value=1, max_value=12, label="Antall tidspunkt", initial=4)
    per_slot = forms.IntegerField(min_value=1, initial=3, label="Antall personer per tidspunkt")
    term = forms.ChoiceField(choices=(("V", "Vår"), ("H", "Høst")), label="Semester")

    def clean(self):
        cleaned_data = super().clean()

        term_shorthand = str(cleaned_data["year"])[-2:] + cleaned_data["term"]
        cleaned_data["term"] = term_shorthand
        if TimeTable.objects.filter(term=term_shorthand).exists():
            raise forms.ValidationError("Det finnes allerede en vaktliste for dette semesteret")

        return cleaned_data
