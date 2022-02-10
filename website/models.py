from datetime import datetime

from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models

from files.models import Image

# Set custom User string representation
User.add_to_class("__str__", lambda u: f"{u.get_full_name()} ({u.username})")


class Card(models.Model):
    title = models.CharField(max_length=100, verbose_name="Title", blank=False)
    body = models.TextField(max_length=200, blank=False)
    thumbnail = models.ForeignKey(Image, on_delete=models.CASCADE, blank=False)
    thumbnail_dark_text = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class FaqQuestion(models.Model):
    question = models.CharField(max_length=100, verbose_name="Spørsmål", blank=False)
    text = models.TextField(max_length=1000, verbose_name="Svar", blank=False)
    icon = models.CharField(
        max_length=30,
        verbose_name="Ikon",
        help_text="Eksempel 'note_add' fra https://material.io/tools/icons/?style=baseline",
        blank=False,
    )

    def __str__(self):
        return self.question


class Rule(models.Model):
    title = models.CharField(max_length=100, verbose_name="Tittel", blank=False)
    body = RichTextField()
    thumb = models.ForeignKey(
        "files.Image",
        blank=True,
        null=True,
        verbose_name="Bilde",
        on_delete=models.SET_NULL,
    )
    internal = models.BooleanField(default=False, verbose_name="Intern regel")
    printer_rule = models.BooleanField(
        default=False, verbose_name="Regel for bruk av printer"
    )
    priority = models.IntegerField(default=0)
    pub_date = models.DateField(verbose_name="Publiseringsdato", auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        permissions = (("can_view_internal_rule", "Can view internal rule"),)


# Banners that can appear on the top of specific sites
class Banner(models.Model):
    text = models.TextField(
        null=False,
        blank=False,
        default="Sample Text",
        max_length=1000,
        verbose_name="bannertext",
        help_text="Tekst som vises i banneret.",
    )
    color = models.CharField(
        null=False,
        blank=False,
        max_length=10,
        default="hs-yellow",
        verbose_name="bannercolor",
        help_text="Bakgrunnsfargen til banneret som en hex-farge. hs-green, hs-yellow og hs-red støttes også som presets.",
    )
    text_color = models.CharField(
        null=False,
        blank=False,
        max_length=10,
        default="hs-black",
        verbose_name="bannertextcolor",
        help_text="Tekstfargen på banneret. hs-white og hs-black støttes som presets.",
    )
    active = models.BooleanField(default=True, verbose_name="aktiv")
    end_date = models.DateField(
        null=True,
        blank=True,
        default=datetime.now,
        verbose_name="sluttdato",
        help_text="Banneret vil ikke vises uansett om den har aktiv status etter denne datoen.",
    )

    site = models.CharField(
        null=False,
        blank=False,
        default="*",
        max_length=250,
        verbose_name="bannersider",
        help_text="Det interne navnet på URL-stien til sidene som banneret skal dukke opp på. Separert med komma (,). Wildcard (*) støttes. F.eks. er '*' ALLE sider, 'inventory:*' er alle lagersider.",
    )

    def __str__(self):
        return "Banner - {} {}".format(self.site, "(Aktiv)" if self.active else "")

    def is_active(self):
        """Returns whether or not this banner should be shown"""
        expired = self.end_date is not None and datetime.now().date() > self.end_date
        return self.active and not expired
