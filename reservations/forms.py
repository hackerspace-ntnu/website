from django import forms

from reservations.models import Reservation


class ReservationForm(forms.ModelForm):

    class Meta:
        model = Reservation
        fields = ['comment', 'start_date', 'end_date', 'start_time', 'end_time']

        labels = {
            'comment': 'Kommentar',
            'start_date': 'Startdato',
            'end_date': 'Sluttdato',
            'start_time': 'Starttid',
            'end_time': 'Sluttid',
        }
