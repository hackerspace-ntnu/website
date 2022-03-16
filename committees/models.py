from django.contrib.auth.models import Group, User
from django.db import models


class Committee(Group):
    # Name feltet er fra superclass
    thumbnail = models.ImageField(
        upload_to="committees", null=True, blank=True, verbose_name="miniatyrbilde"
    )
    description = models.TextField(verbose_name="beskrivelse")

    email = models.EmailField(blank=True, null=True)

    main_lead = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL, related_name="Leder"
    )
    second_lead = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL, related_name="Nestleder"
    )
    economy = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="Økonomiansvarlig",
    )

    active = models.BooleanField()

    priority = models.IntegerField(default=0)
