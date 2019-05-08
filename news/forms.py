from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from ckeditor.widgets import CKEditorWidget
from datetime import datetime
from django.core.exceptions import ValidationError
from files.models import Image
from news.models import Event, EventRegistration
from django.forms import inlineformset_factory
from django.contrib.auth.models import User

custom_error = {
    'required': '',
}

class EventAttendeeForm(forms.ModelForm):
    # Til registrering av attendees
    def __init__(self, *args, **kwargs):
        super(EventAttendeeForm, self).__init__(*args, **kwargs)
        if kwargs.get('instance'):
            if kwargs.get('instance').is_waitlisted():
                self.fields['user'].label = kwargs.get('instance').user.get_full_name() + " (Venteliste) "
            else:
                self.fields['user'].label = kwargs.get('instance').user.get_full_name()

    class Meta:
        model = EventRegistration
        fields = ['attended', 'user', 'event', 'date']


eventformset = inlineformset_factory(Event, EventRegistration,
        form=EventAttendeeForm, extra=0)

class SplitDateTimeFieldCustom(forms.SplitDateTimeField):
    '''
        Dette er en custom SplitDateTimeField som respekterer norske datoformat
    '''
    widget=forms.SplitDateTimeWidget(
            date_attrs=({
                'class': 'no-autoinit datepicker',
                }),
            date_format='%Y-%m-%d',
            time_format='%H:%M',
            )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, input_date_formats=['%Y-%m-%d',], input_time_formats=['%H:%M',])



class EventForm(forms.ModelForm):
    error_css_class = 'invalid'
    time_start = SplitDateTimeFieldCustom()
    time_end = SplitDateTimeFieldCustom()

    registration_start = SplitDateTimeFieldCustom()
    deregistration_end = SplitDateTimeFieldCustom()

    class Meta:
        model = Event
        fields = ['title', 'main_content', 'ingress_content', 'thumbnail', 'internal', 'registration', 'max_limit', 'registration_start', 'deregistration_end', 'external_registration',
                  'time_start', 'time_end', 'place', 'servering', 'place_href']











