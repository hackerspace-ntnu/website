from django.contrib.auth.admin import User
from django.db.models.signals import post_save
from django.core.files.base import ContentFile
from django.dispatch import receiver
from django.db import models
from django.shortcuts import reverse
from datetime import datetime
from sorl.thumbnail import get_thumbnail
from applications.validators import validate_phone_number
from django.utils import timezone
from ckeditor.fields import RichTextField


class TermsOfService(models.Model):

    text = RichTextField(config_name="tos_editor")
    pub_date = models.DateField(default=timezone.now, verbose_name='Publiseringsdato');

    def __str__(self):
        return self.pub_date.strftime('%d. %B %Y')


class Skill(models.Model):

    name = models.CharField(max_length=50)
    description = models.TextField()
    thumb = models.ForeignKey('files.Image', blank=True, null=True, on_delete=models.SET_NULL)

    category = models.ManyToManyField(blank=False, to='userprofile.Category')

    prerequisites = models.ManyToManyField(blank=True, to='userprofile.Skill')

    def __str__(self):
        return self.name

class Category(models.Model):

    name = models.CharField(max_length=30)
    description = models.TextField()
    thumb = models.ForeignKey('files.Image', blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    image = models.ImageField(upload_to="profilepictures", verbose_name="Profilbilde", default=None, blank=True)

    skills = models.ManyToManyField(blank=True, verbose_name="Ferdigheter", to='userprofile.Skill')

    # Felter for sosiale konti
    social_discord = models.CharField(max_length=30, null=True, blank=True, verbose_name="Discord-tag")
    social_steam = models.CharField(max_length=30, null=True, blank=True, verbose_name="Steam navn")
    social_battlenet = models.CharField(max_length=30, null=True, blank=True, verbose_name="Battle.net-tag")
    social_git = models.CharField(max_length=30, null=True, blank=True, verbose_name="Github brukernavn")

    limit_social = models.BooleanField(default=False, verbose_name="Vis sosiale profiler kun for andre Hackerspace-medlemmer")

    access_card = models.CharField(max_length=20, null=True, blank=True, verbose_name="NTNU Adgangskort (EMXXXXXXXXXX)")
    study = models.CharField(max_length=50, null=True, blank=True, verbose_name="Studieretning")

    accepted_tos = models.ForeignKey(TermsOfService, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Seneste aksepterte TOS")

    phone_number = models.CharField(max_length=8, null=True, blank=True, validators=[validate_phone_number], verbose_name="Telefonnummer",
                                    help_text="Brukes til reservasjonssystem i tilfelle du må kontaktes.")

    show_email = models.BooleanField(default=False, verbose_name="Vis epostadresse i din profil")

    allergi_gluten = models.BooleanField(default=False, verbose_name="Ønsker glutenfritt alternativ")
    allergi_vegetar = models.BooleanField(default=False, verbose_name="Ønsker vegetar alternativ")
    allergi_vegan = models.BooleanField(default=False, verbose_name="Ønsker vegansk alternativ")
    allergi_annet = models.CharField(max_length=140, null=True, blank=True, verbose_name="Evt. andre ønsker for matservering.")

    class Meta:
        permissions =  (
                ("can_view_social", "Can see social fields on UserProfile"),
                ("can_view_admin", "Can see information for admin panel"),
                )

    def save(self, *args, **kwargs):
        if self.image:
            # Make sure image is saved before tumbnailing
            super(Profile, self).save(*args, **kwargs)
            thumb = get_thumbnail(self.image, '300x300', crop='center', quality=99)
            self.image.save(thumb.name, ContentFile(thumb.read()), False)
        super(Profile, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username

    def get_main_group(self):
        return self.user.groups.first()

    def get_absolute_url(self):
        return reverse('userprofile:profile', args=(self.pk,))

    def has_accepted_most_recent_tos(self):
        return self.accepted_tos == TermsOfService.objects.order_by('-pub_date').first();
