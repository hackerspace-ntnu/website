import datetime

from django.forms import ModelForm, ValidationError

from reservations.models import Queue, Reservation


class QueueForm(ModelForm):

    class Meta:
        model = Queue
        fields = '__all__'

    def clean(self):
        start_time = self.cleaned_data.get('start_time', None)
        end_time = self.cleaned_data.get('end_time', None)

        if start_time > end_time:
            raise ValidationError("Your queue must start before it can end")


class ReservationForm(ModelForm):

    class Meta:
        model = Reservation
        fields = ('date', 'start_time', 'end_time', )

    def clean(self):
        start_time = self.cleaned_data.get('start_time', None)
        end_time = self.cleaned_data.get('end_time', None)
        date = self.cleaned_data.get('date', None)

        if start_time > end_time:
            raise ValidationError("Your queue must start before it can end")

        if date < datetime.date.today():
            raise ValidationError("You cannot make reservations back in time")
