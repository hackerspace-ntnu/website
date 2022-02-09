from django import forms
from django.contrib.auth.models import User
from django.db.utils import OperationalError, ProgrammingError
from django.forms import inlineformset_factory
from django.forms.widgets import ClearableFileInput
from django.utils import timezone

from committees.models import Committee
from news.models import Article, Event, EventRegistration, Upload


class EventAttendeeForm(forms.ModelForm):
    # Til registrering av attendees
    def __init__(self, *args, **kwargs):
        super(EventAttendeeForm, self).__init__(*args, **kwargs)
        if kwargs.get("instance"):
            if kwargs.get("instance").is_waitlisted():
                self.fields["user"].label = (
                    kwargs.get("instance").user.get_full_name() + " (Venteliste) "
                )
            else:
                self.fields["user"].label = kwargs.get("instance").user.get_full_name()

    class Meta:
        model = EventRegistration
        fields = ["attended", "user", "event", "date"]


eventformset = inlineformset_factory(
    Event, EventRegistration, form=EventAttendeeForm, extra=0
)


class SplitDateTimeFieldCustom(forms.SplitDateTimeField):
    """
    Dette er en custom SplitDateTimeField som respekterer norske datoformat
    """

    widget = forms.SplitDateTimeWidget(
        date_attrs=(
            {
                "class": "no-autoinit datepicker",
            }
        ),
        date_format="%Y-%m-%d",
        time_format="%H:%M",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            **kwargs,
            input_date_formats=[
                "%Y-%m-%d",
            ],
            input_time_formats=[
                "%H:%M",
            ]
        )


class UserFullnameChoiceField(forms.ModelChoiceField):
    """
    Denne klassen overrider ModelChoiceField for å vise vanlige
    fulle navn istedenfor brukernavn
    """

    def label_from_instance(self, obj):
        return obj.get_full_name()


class MaterialFileWidget(ClearableFileInput):
    template_name = "files/_file_widget.html"


class UploadForm(forms.ModelForm):
    file = forms.FileField(
        label="Legg ved fil", required=False, widget=MaterialFileWidget
    )

    class Meta:
        model = Upload
        fields = ["title", "file"]


def get_committees():
    try:
        return list(Committee.objects.values_list("name", flat=True))
    except OperationalError:
        return []
    except ProgrammingError:
        return []


class UpdatePubDateOnDraftPublishMixin(forms.ModelForm):
    """
    Form mixin for updating publishing date when draft is published
    """

    def save(self, commit=True):
        # Check if draft status has been changed
        if "draft" in self.changed_data:
            # Check if changed to non-draft (i.e. published)
            if not self.cleaned_data["draft"]:
                # Update publishing date
                self.instance.pub_date = timezone.now()
        return super().save(commit)


class EventForm(UpdatePubDateOnDraftPublishMixin, forms.ModelForm):
    error_css_class = "invalid"

    ingress_content = forms.CharField(
        widget=forms.Textarea(attrs={"class": "materialize-textarea"}),
        label="Ingress",
        help_text="En kort introduksjon til teksten",
    )

    time_start = SplitDateTimeFieldCustom(label="Starttidspunkt")
    time_end = SplitDateTimeFieldCustom(label="Sluttidspunkt")

    registration_start = SplitDateTimeFieldCustom(label="Påmeldingsstart")
    registration_end = SplitDateTimeFieldCustom(label="Påmeldingsfrist")
    deregistration_end = SplitDateTimeFieldCustom(label="Avmeldingsfrist")

    responsible = UserFullnameChoiceField(
        label="Arrangementansvarlig",
        queryset=User.objects.all()
        .filter(groups__name__in=get_committees())
        .order_by("first_name"),
    )

    class Meta:
        model = Event
        fields = [
            "title",
            "main_content",
            "ingress_content",
            "thumbnail",
            "responsible",
            "internal",
            "registration",
            "max_limit",
            "registration_start",
            "registration_end",
            "deregistration_end",
            "external_registration",
            "time_start",
            "time_end",
            "place",
            "servering",
            "place_href",
            "draft",
        ]


class ArticleForm(UpdatePubDateOnDraftPublishMixin, forms.ModelForm):

    ingress_content = forms.CharField(
        widget=forms.Textarea(attrs={"class": "materialize-textarea"}),
        label="Ingress",
        help_text="En kort introduksjon til teksten",
    )

    class Meta:
        model = Article
        fields = [
            "title",
            "ingress_content",
            "main_content",
            "thumbnail",
            "internal",
            "draft",
        ]


uploadformset = inlineformset_factory(Event, Upload, form=UploadForm, extra=3)
