# Create your models here.
from ckeditor.fields import RichTextField
from django.db import models
from files.models import Image
from datetime import datetime




class Project():
    name = models.CharField(max_length=100, verbose_name='Name', blank=False)
    body = models.TextField(max_length=200, blank=False)
    thumbnail = models.ForeignKey(Image, on_delete=models.CASCADE, blank=False)
    thumbnail_dark_text = models.BooleanField(default=False)

    def __str__(self):
        return self.title




