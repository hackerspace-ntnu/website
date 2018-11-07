import datetime

from django.forms import ModelForm, ValidationError, TimeInput, DateInput
from django.shortcuts import get_object_or_404

from reservations.models import Queue, Reservation


class QueueForm(ModelForm):

    class Meta:
        model = Queue
        fields = '__all__'


class ReservationForm(ModelForm):

    class Meta:
        model = Reservation
        fields = ('date', 'start_time', 'end_time', )
        widgets = {
            'date': DateInput(attrs={'class': 'datepicker .no-autoinit'}),
            'start_time': TimeInput(attrs={'class': 'timepicker .no-autoinit'}),
            'end_time': TimeInput(attrs={'class': 'timepicker .no-autoinit'}),
        }

    def __init__(self, *args, **kwargs):
        self.parent_queue = get_object_or_404(Queue, pk=kwargs.pop('pk'))
        super().__init__(*args, **kwargs)

    def clean(self):

        cleaned_data = super(ReservationForm, self).clean()

        start_time = cleaned_data.get('start_time', None)
        end_time = cleaned_data.get('end_time', None)
        date = cleaned_data.get('date', None)

        if start_time > end_time:
            raise ValidationError("Invalid argument parameters")

        if date < datetime.date.today() \
                or (start_time < (datetime.datetime.now() - datetime.timedelta(minutes=5)).time()
                    and date == datetime.date.today()):
            raise ValidationError("You cannot make reservations back in time")

        for interval in [(r.start_time, r.end_time) for r in self.parent_queue.reservations.filter(date=date)]:
            reservation_overlap = interval[0] <= start_time, end_time <= interval[1]
            if reservation_overlap.__contains__(True):
                raise ValidationError("Reservation incompatible with existing reservations")

        return cleaned_data
