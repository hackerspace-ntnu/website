from django.db import models
import datetime


class Application(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.PositiveIntegerField()
    study_program = models.CharField(max_length=255)
    year = models.SmallIntegerField()
    knownledge_of_hackerspace = models.TextField()
    choice_of_group = models.CharField()
    about = models.TextField()
    application_text = models.TextField()
    application_date = models.DateTimeField(default=datetime.now())

