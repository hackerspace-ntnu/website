from django.db import models
from django.contrib.auth.admin import User


class Skill(models.Model):
    title = models.CharField(max_length=30)
    icon = models.ImageField(upload_to="skillicons")

    def __str__(self):
        return self.title


class Group(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class DutyTime(models.Model):
    MONDAY = 'MA'
    TUESDAY = 'TU'
    WEDNESDAY = 'WE'
    THURSDAY = 'TH'
    FRIDAY = 'FR'

    DUTYDAYS_CHOICES = (
        (MONDAY, 'Mandag'),
        (TUESDAY, 'Tirsdag'),
        (WEDNESDAY, 'Onsdag'),
        (THURSDAY, 'Torsdag'),
        (FRIDAY, 'Fredag')
    )

    day = models.CharField(max_length=2, choices=DUTYDAYS_CHOICES, default=MONDAY)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return self.day + " " + str(self.start_time) + "-" + str(self.end_time)


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    image = models.ImageField(upload_to="profilepictures")
    group = models.ManyToManyField(Group, related_name="members")
    access_card = models.CharField(max_length=20, null=True, blank=True)
    skills = models.ManyToManyField(Skill)
    study = models.TextField(null=True, blank=True)
    dutytime = models.ManyToManyField(DutyTime)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name
