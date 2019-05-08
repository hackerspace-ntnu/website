from django.db import models
from files.models import Image

class Card(models.Model):
    title = models.CharField(max_length=100, verbose_name='Title', blank=False)
    body = models.TextField(max_length=200, blank=False)
    thumbnail = models.ForeignKey(Image, on_delete=models.CASCADE, blank=False)
    thumbnail_dark_text = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class FaqQuestion(models.Model):
    question = models.CharField(max_length=100, verbose_name='Spørsmål', blank=False)
    text = models.TextField(max_length=1000, verbose_name='Svar', blank=False)
    icon = models.CharField(max_length=30, verbose_name='Ikon', help_text="Eksempel 'note_add' fra https://material.io/tools/icons/?style=baseline", blank=False)

    def __str__(self):
        return self.question
