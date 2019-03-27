from django import forms

from reservations.models import Reservation


class ReservationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['parent_queue'].widget = forms.HiddenInput()

    class Meta:
        model = Reservation
        fields = ['start', 'end', 'comment', 'parent_queue']
