from django import forms
from news.models import Event, EventRegistration
from django.forms import inlineformset_factory
from django.contrib.auth.models import User
from committees.models import Committee

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
    widget = forms.SplitDateTimeWidget(
            date_attrs=({
                'class': 'no-autoinit datepicker',
                }),
            date_format='%Y-%m-%d',
            time_format='%H:%M',
            )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, input_date_formats=['%Y-%m-%d',], input_time_formats=['%H:%M',])


class UserFullnameChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.get_full_name()


class EventForm(forms.ModelForm):
    error_css_class = 'invalid'
    time_start = SplitDateTimeFieldCustom()
    time_end = SplitDateTimeFieldCustom()

    registration_start = SplitDateTimeFieldCustom()
    registration_end = SplitDateTimeFieldCustom()
    deregistration_end = SplitDateTimeFieldCustom()

    committee_array = Committee.objects.values_list('name', flat=True)
    responsible = UserFullnameChoiceField(queryset=User.objects.all().filter(groups__name__in=list(committee_array)).order_by('first_name'))

    class Meta:
        model = Event
        fields = ['title', 'main_content', 'ingress_content', 'thumbnail', 'responsible', 'internal', 'registration', 'max_limit', 'registration_start', 'registration_end', 'deregistration_end', 'external_registration',
                  'time_start', 'time_end', 'place', 'servering', 'place_href']











