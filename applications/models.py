from datetime import datetime

from django.db import models
from django.utils import timezone
from applications.validators import validate_phone_number


class Application(models.Model):

    # CHANGE THIS DATE TO ALLOW APPLICATIONS
    APPLICATION_DEADLINE = datetime(2017, 9, 4, 1, 0, 0)

    YEAR_CHOICES = ((1, 1),
                    (2, 2),
                    (3, 3),
                    (4, 4),
                    (5, 5),
                    )

    GROUP_CHOICES = (("DEVOPS", "DEVOPS"),
                     ("PR", "PR"),
                     ("LABOPS", "LABOPS"),
                     ("ER", "ER"),
                     ("VR", "VR"),
                     )

    name = models.CharField(max_length=50, verbose_name="Navn")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=8, validators=[validate_phone_number], verbose_name="Telefon")
    study = models.CharField(max_length=255, verbose_name="Studieprogram")
    year = models.IntegerField(verbose_name="Årstrinn", choices=YEAR_CHOICES, default=YEAR_CHOICES[0])
    group_choice = models.CharField(max_length=255, choices=GROUP_CHOICES, verbose_name="Ønsket gruppe")
    knowledge_of_hs = models.CharField(max_length=1000, verbose_name="Hvordan fikk du vite om Hackerspace?")
    about = models.TextField(verbose_name="Litt om deg selv")
    application_text = models.TextField(verbose_name="Hvorfor søker du hackerspace?")
    application_date = models.DateTimeField(default=timezone.now, blank=False)

    def __str__(self):
        return self.name


class ProjectApplication(models.Model):
    email = models.EmailField(verbose_name="Email")

    def __str__(self):
        return self.email
