from django.forms import ModelForm

from reservations.models import Queue


class QueueForm(ModelForm):

    class Meta:
        model = Queue
        fields = '__all__'

