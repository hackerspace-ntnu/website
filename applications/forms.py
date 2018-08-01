from django.forms import ModelForm, Textarea
from django.core.mail import send_mail
from django.template.loader import render_to_string

from .models import Application


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
            'application_text': Textarea(attrs={'class': 'materialize-textarea'})
        }

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
