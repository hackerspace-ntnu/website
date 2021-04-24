from django.forms import ModelForm, Textarea, TextInput
from django.core.mail import send_mail
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
        fields = ['name',
                  'email',
                  'phone',
                  'study',
                  'year',
                  'group_choice',
                  'knowledge_of_hs',
                  'about',
                  'application_text',
                  ]
        widgets = {
            'about': Textarea(attrs={'class': 'materialize-textarea'}),
            'application_text': Textarea(attrs={'class': 'materialize-textarea'}),
            'group_choice': ApplicationGroupChoiceField(attrs={'id': 'groups-chosen-input', 'type': 'hidden'})
        }

    def save(self, commit=True):
        super().save(commit)
        # Attach priority to group choices
        group_choice = list(map(int, self.data['group_choice'].split(",")))
        for choice in ApplicationGroupChoice.objects.filter(application=self.instance.id):
            choice.priority = group_choice.index(choice.group.id)
            choice.save()

    def send_email(self):
        plain_message = render_to_string('applications/application_success_mail.txt', {
            'navn': self.cleaned_data['name'],
            'grupper': self.cleaned_data['group_choice']
        })

        send_mail(
            '[Hackerspace NTNU] Søknad er registrert!',
            plain_message,
            'Hackerspace NTNU',
            [self.cleaned_data['email']],
            fail_silently=False,
        )
        pass
