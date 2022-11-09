from django.db import models
from markdownx.models import MarkdownxField

from files.models import Image


class Equipment(models.Model):
    """Types of equipment that the workshop has and provides"""

    name = models.CharField(max_length=255, verbose_name="Navn")
    description = MarkdownxField(blank=True, verbose_name="Beskrivelse")
    inventory_link = models.URLField(
        verbose_name="Lenke til lagersystemet", blank=True, null=True
    )
    thumbnail = models.ForeignKey(
        Image, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Bilde"
    )
