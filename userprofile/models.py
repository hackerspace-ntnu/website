from django.contrib.auth.admin import User
from django.db.models.signals import post_save
from django.core.files.base import ContentFile
from django.dispatch import receiver
from django.db import models
from django.shortcuts import reverse

from datetime import datetime
from sorl.thumbnail import get_thumbnail

from vaktliste.views import vakt_filter


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


class Group(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class DutyTime(models.Model):
    MONDAY = 'Mandag'
    TUESDAY = 'Tirsdag'
    WEDNESDAY = 'Onsdag'
    THURSDAY = 'Torsdag'
    FRIDAY = 'Fredag'

    DUTYDAYS_CHOICES = (
        (MONDAY, 'Mandag'),
        (TUESDAY, 'Tirsdag'),
        (WEDNESDAY, 'Onsdag'),
        (THURSDAY, 'Torsdag'),
        (FRIDAY, 'Fredag')
    )

    day = models.CharField(max_length=7, choices=DUTYDAYS_CHOICES, default=MONDAY)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def shorten_time(self, time):
        return ":".join(str(time).split(":")[:2])

    def dutyday(self):
        return [dutyday[1] for dutyday in self.DUTYDAYS_CHOICES if dutyday[0] == self.day][0]

    def dutytime(self):
        return self.shorten_time(self.start_time) + " - " + self.shorten_time(self.end_time)

    def __str__(self):
        return self.day + " " + str(self.start_time) + "-" + str(self.end_time)


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    group = models.ManyToManyField(Group, related_name='profile', verbose_name="Gruppe", blank=True)
    image = models.ImageField(upload_to="profilepictures", verbose_name="Profilbilde", default=None, blank=True)

    access_card = models.CharField(max_length=20, null=True, blank=True)
    study = models.CharField(max_length=50, null=True, blank=True)
    skills = models.ManyToManyField(Skill, related_name="skills", blank=True)
    duty = models.ManyToManyField(DutyTime, related_name="duty", blank=True)

    auto_duty = models.BooleanField(default=True)
    tos_accepted = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.image:
            # Make sure image is saved before tumbnailing
            super(Profile, self).save(*args, **kwargs)
            thumb = get_thumbnail(self.image, '300x300', crop='center', quality=99)
            self.image.save(thumb.name, ContentFile(thumb.read()), False)
        super(Profile, self).save(*args, **kwargs)

    def get_dutytime(self):
        if self.auto_duty:
            result = vakt_filter(persons=self.user.get_full_name(), output="tuples")
            if result:
                day, time, hackers = result[0]
                start_time, end_time = time.split(" - ")
                start_time = datetime.strptime(start_time, "%H:%M")
                end_time = datetime.strptime(end_time, "%H:%M")
                try:
                    self.duty = [DutyTime.objects.get(day=day, start_time=start_time, end_time=end_time)]
                except:
                    duty = [DutyTime.objects.create(day=day, start_time=start_time, end_time=end_time)]
                    self.duty = duty

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('userprofile:profile', args=(self.pk,))



# Save a user profile whenever we create a user
@receiver(post_save, sender=User, dispatch_uid="create_profile_on_user_create")
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, auto_duty=False, tos_accepted=True)
