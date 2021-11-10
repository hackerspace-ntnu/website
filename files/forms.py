from django.forms import ModelForm
from django.forms import TextInput
from .models import Image


class ImageForm(ModelForm):
    class Meta:
        model = Image
        fields = ["title", "img_category", "file"]
