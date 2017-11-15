from django.db import models
from django.contrib.auth.admin import User
from vaktliste.views import vakt_filter
from datetime import datetime

class Skill(models.Model):
    title = models.CharField(max_length=30)
    icon = models.ImageField(upload_to="skillicons",blank=True)
    description = models.TextField()

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

    def shorten_time(self,time):
        return ":".join(str(time).split(":")[:2])

    def dutyday(self):
        return [dutyday[1] for dutyday in self.DUTYDAYS_CHOICES if dutyday[0]==self.day][0]

    def dutytime(self):
        return self.shorten_time(self.start_time) + " - " + self.shorten_time(self.end_time)

    def __str__(self):
        return self.day + " " + str(self.start_time) + "-" + str(self.end_time)


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    group = models.ManyToManyField(Group, related_name="groups",blank=True)
    name = models.CharField(max_length=30, null=True, blank=True)
    image = models.ImageField(upload_to="profilepictures",default="profilepictures/default.jpg")
    
    access_card = models.CharField(max_length=20, null=True, blank=True)
    study = models.CharField(max_length=50, null=True, blank=True)
    skills = models.ManyToManyField(Skill, related_name="skills",blank=True)
    duty = models.ManyToManyField(DutyTime, related_name="duty",blank=True)
    
    auto_duty = models.BooleanField(default=True)
    auto_name = models.BooleanField(default=True)

    def update(self):
        if self.auto_name: self.name = self.user.first_name + " " + self.user.last_name
        self.email = self.user.email
        self.get_dutytime()
        self.save()

    
    def get_dutytime(self):
        if self.auto_duty:
            result = vakt_filter(persons=str(self))
            for day in result:
                for time in result[day]:
                    start_time,end_time = time.split(" - ")
                    start_time= datetime.strptime(start_time,"%H:%M")
                    end_time= datetime.strptime(end_time,"%H:%M")
                    try:
                        self.duty = [DutyTime.objects.get(day=day,start_time=start_time,end_time=end_time)]
                    except:
                        duty = [DutyTime.objects.create(day=day, start_time=start_time, end_time=end_time)]
                        self.duty = duty
                    break

    def __str__(self):
        return self.name
