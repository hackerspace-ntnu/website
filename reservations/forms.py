from django import forms

from reservations.models import Reservation


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ('start', 'end', 'comment')
