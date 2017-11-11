from django.db import models
from django.contrib.auth.admin import User


class Skill(models.Model):
    title = models.CharField(max_length=30)
    icon = models.ImageField(upload_to="skillicons")
    description = models.TextField()

    def __str__(self):
        return self.title


"""
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
"""


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    #group = models.ManyToManyField(Group, related_name="groups")
    name = models.CharField(max_length=30, null=True, blank=True)
    image = models.ImageField(upload_to="website/static/img/profilepictures")

    access_card = models.CharField(max_length=20, null=True, blank=True)
    skills = models.ManyToManyField(Skill, related_name="skills")
    study = models.TextField(null=True, blank=True)
    #dutytime = models.ManyToManyField(DutyTime)

    def __str__(self):
        self.name = self.user.first_name + " " + self.user.last_name
        return self.name
