from datetime import datetime

from django.db import models
from django.utils import timezone

from applications.validators import validate_phone_number

YEAR_CHOICES = (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
)


class ApplicationPeriod(models.Model):
    name = models.CharField(max_length=50, verbose_name="Navn")
    period_start = models.DateTimeField(default=timezone.now, blank=False)
    period_end = models.DateTimeField(default=timezone.now, blank=False)

    def __str__(self):
        return self.name

    def status(self):
        if self.period_end < datetime.now():
            return "late"
        elif datetime.now() < self.period_start:
            return "early"
        return "open"

    def is_open(self):
        return self.status() == "open"


class ApplicationGroup(models.Model):
    name = models.CharField(max_length=50, verbose_name="Gruppenavn")
    text_main = models.TextField(verbose_name="Om gruppen generelt", blank=False)
    text_structure = models.TextField(verbose_name="Om gruppens struktur", blank=True)
    text_workload = models.TextField(
        verbose_name="Om gruppens arbeidsmengde", blank=True
    )
    project_group = models.BooleanField(
        verbose_name="Gruppen tilhører prosjektgruppen", default=False
    )
    open_for_applications = models.BooleanField(
        verbose_name="Åpen for søknader", default=True
    )

    def __str__(self):
        return self.name


class Application(models.Model):
    name = models.CharField(max_length=50, verbose_name="Navn")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(
        max_length=20, validators=[validate_phone_number], verbose_name="Telefon"
    )
    study = models.CharField(max_length=255, verbose_name="Studieprogram")

    year = models.IntegerField(
        blank=False,
        verbose_name="Årstrinn",
        choices=YEAR_CHOICES,
        default=YEAR_CHOICES[0],
    )

    knowledge_of_hs = models.CharField(
        max_length=1000, verbose_name="Hvordan fikk du vite om Hackerspace?"
    )

    about = models.TextField(verbose_name="Litt om deg selv")

    application_text = models.TextField(verbose_name="Hvorfor søker du hackerspace?")

    group_choice = models.ManyToManyField(
        ApplicationGroup, through="ApplicationGroupChoice", blank=True
    )

    project_interests = models.TextField(
        verbose_name="Er det andre prosjekter du er interessert i?", default=""
    )

    application_date = models.DateTimeField(default=timezone.now, blank=False)

    def __str__(self):
        return self.name


class ApplicationGroupChoice(models.Model):
    """Intermediate model to add priority attribute to application group choices"""

    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    group = models.ForeignKey(ApplicationGroup, on_delete=models.CASCADE)
    priority = models.PositiveIntegerField(null=True)

    class Meta:
        ordering = ["priority"]
