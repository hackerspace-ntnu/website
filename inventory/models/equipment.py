from bleach import clean
from bleach_whitelist import markdown_attrs, markdown_tags
from django.db import models
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
from ordered_model.models import OrderedModel

from files.models import Image


class Equipment(OrderedModel):
    """Types of equipment that the workshop has and provides"""

    name = models.CharField(max_length=255, verbose_name="Navn")
    description = MarkdownxField(blank=True, verbose_name="Beskrivelse")
    inventory_link = models.URLField(
        verbose_name="Lenke til lagersystemet", blank=True, null=True
    )
    thumbnail = models.ForeignKey(
        Image, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Bilde"
    )

    def formatted_markdown(self):
        return clean(markdownify(self.description), markdown_tags, markdown_attrs)
