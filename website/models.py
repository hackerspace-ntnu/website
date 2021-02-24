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

# Banners that can appear on the top of specific sites
class Banner(models.Model):
    text = models.TextField(
        null=True,
        blank=True,
        max_length=1000,
        verbose_name="bannertext",
        help_text="Tekst som vises i banneret."
    )
    color = models.CharField(
        null=True,
        blank=True,
        max_length=10,
        default="hs-yellow",
        verbose_name="bannercolor",
        help_text="Bakgrunnsfargen til banneret som en hex-farge. hs-green, hs-yellow og hs-red støttes også som presets."
    )
    text_color = models.CharField(
        null=True,
        blank=True,
        max_length=10,
        default='hs-black',
        verbose_name="bannertextcolor",
        help_text="Tekstfargen på banneret. hs-white og hs-black støttes som presets."
    )
    active = models.BooleanField(default=True, verbose_name="aktiv")

    site = models.CharField(
        null=True,
        blank=True,
        max_length=250,
        verbose_name="bannersite",
        help_text="Det interne navnet på URL-stien til siden som banneret skal dukke opp på. Wildcard (*) støttes. F.eks. er '*' ALLE sider, 'inventory:*' er alle lagersider."
    )

    def __str__(self):
        return 'Banner - {} {}'.format(self.site, '(Aktiv)' if self.active else '')
