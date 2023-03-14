from django.core.mail import send_mail
from django.forms import ModelForm, Textarea, TextInput
from django.template.loader import render_to_string

from .models import Application, ApplicationGroupChoice


class ApplicationGroupChoiceField(TextInput):
    def value_from_datadict(self, data, files, name):
        value = data.get(name)
        if value:
            return value.split(",")


class ApplicationForm(ModelForm):
    class Meta:
        model = Application
        fields = [
            "name",
            "email",
            "phone",
            "study",
            "year",
            "group_choice",
            "knowledge_of_hs",
            "about",
            "application_text",
            "project_interests",
        ]
        widgets = {
            "about": Textarea(
                attrs={"class": "materialize-textarea", "style": "height: 150px;"}
            ),
            "application_text": Textarea(
                attrs={"class": "materialize-textarea", "style": "height: 150px;"}
            ),
            "project_interests": Textarea(
                attrs={"class": "materialize-textarea", "style": "height: 150px;"}
            ),
            "group_choice": ApplicationGroupChoiceField(
                attrs={"id": "groups-chosen-input", "type": "hidden"}
            ),
        }

    def save(self, commit=True):
        super().save(commit)
        # Attach priority to group choices
        group_choice_str = self.data["group_choice"]

        if group_choice_str:
            group_choice = list(map(int, group_choice_str.split(",")))
            for choice in ApplicationGroupChoice.objects.filter(
                application=self.instance.id
            ):
                choice.priority = group_choice.index(choice.group.id) + 1
                choice.save()

    def send_email(self):

        # Retrieve group choice with priorities (assumes that save() has been run first)
        group_choice = ApplicationGroupChoice.objects.filter(
            application=self.instance.id
        ).order_by("priority")

        plain_message = render_to_string(
            "applications/application_success_mail.txt",
            {"name": self.cleaned_data["name"], "group_choice": group_choice},
        )

        send_mail(
            "[Hackerspace NTNU] Søknad er registrert!",
            plain_message,
            "Hackerspace NTNU",
            [self.cleaned_data["email"]],
            fail_silently=False,
        )
        pass
