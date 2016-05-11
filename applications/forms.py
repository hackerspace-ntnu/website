from django.forms import ModelForm
from .models import Application


class ApplicationForm(ModelForm):
    class Meta:
        model = Application
        fields = ['name',
                  'email',
                  'phone',
                  'study_program',
                  'year',
                  'knowledge_of_hackerspace',
                  'choice_of_group',
                  'about',
                  'application_text',
        ]