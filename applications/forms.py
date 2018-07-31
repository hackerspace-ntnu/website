from django.forms import ModelForm
from django.core.mail import send_mail

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

    def send_email(self):
        send_mail(
            '[Hackerspace NTNU] Søknad er registrert!',
            """Hei!

            Dette er en bekreftelse på at din søknad er registrert.
            Vi svarer på søknader fortløpende etter søknadsfristen går ut.


            Tusen takk for din interesse. :-)

            Mvh,
            Styret i Hackerspace NTNU

            """,
            'Hackerspace NTNU',
            [self.cleaned_data['email']],
            fail_silently=False,
        )
        pass
