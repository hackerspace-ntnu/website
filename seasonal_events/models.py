from django.db import models

import datetime
# Create your models here.


class Season(models.Model):
    name = models.CharField(max_length=50, verbose_name="navn")
    start_date = models.DateTimeField(verbose_name="startdato")
    end_date = models.DateTimeField(verbose_name="sluttdato")
    manual_override = models.BooleanField()

    def isNow(self):
        if self.start_date <= datetime.now() <= self.end_date:
            return True
        else:
            return False

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Seasons"

