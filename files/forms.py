from django.forms import ModelForm
from django.forms import TextInput
from .models import Image

class ImageForm(ModelForm):
    class Meta:
        model = Image
        fields = ['description', 'title', 'tags', 'file']
        widgets = {
            'description': TextInput()
        }


