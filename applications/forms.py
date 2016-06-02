from django.forms import ModelForm
from .models import Application


class ApplicationForm(ModelForm):

    year_choices = [choice[1] for choice in Application.YEAR_CHOICES]
    group_choices = [choice[1] for choice in Application.GROUP_CHOICES]

    class Meta:
        model = Application
        fields = ['name',
                  'email',
                  'phone',
                  'study',
                  'group_choice',
                  'year',
                  'knowledge_of_hs',
                  'about',
                  'application_text',
                  ]
        error_messages = {}

        for field in fields:
            error_messages[field] = {'required': 'Feltet må fylles ut', 'invalid_choice': 'Verdien er ikke gyldig'}




