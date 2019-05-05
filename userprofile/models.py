from django.contrib.auth.admin import User
from django.db.models.signals import post_save
from django.core.files.base import ContentFile
from django.dispatch import receiver
from django.db import models
from django.shortcuts import reverse
from datetime import datetime
from sorl.thumbnail import get_thumbnail


class Skill(models.Model):
    title = models.CharField(max_length=30)
    icon = models.ImageField(upload_to="skillicons", blank=True)
    description = models.TextField()

    def save(self, *args, **kwargs):
        if self.icon:
            # Make sure image is saved before tumbnailing
            super(Skill, self).save(*args, **kwargs)
            thumb = get_thumbnail(self.icon, '50x50', crop='center', quality=99)
            self.icon.save(thumb.name, ContentFile(thumb.read()), False)
        super(Skill, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    image = models.ImageField(upload_to="profilepictures", verbose_name="Profilbilde", default=None, blank=True)

    # Felter for sosiale konti
    social_discord = models.CharField(max_length=30, null=True, blank=True, verbose_name="Discord-tag")
    social_steam = models.CharField(max_length=30, null=True, blank=True, verbose_name="Steam navn")
    social_battlenet = models.CharField(max_length=30, null=True, blank=True, verbose_name="Battle.net-tag")
    social_git = models.CharField(max_length=30, null=True, blank=True, verbose_name="Git navn")

    access_card = models.CharField(max_length=20, null=True, blank=True)
    study = models.CharField(max_length=50, null=True, blank=True)
    skills = models.ManyToManyField(Skill, related_name="skills", blank=True)
    tos_accepted = models.BooleanField(default=False)

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
