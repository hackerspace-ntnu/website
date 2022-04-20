from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.admin import User
from django.core.validators import MaxLengthValidator
from django.db import models
from django.db.models import Q
from django.utils import timezone

from files.models import Image


class ProjectarticleManager(models.Manager):
    def search(self, query: str = None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (
                Q(title__icontains=query)
                | Q(main_content__icontains=query)
                | Q(ingress_content__icontains=query)
                | Q(author__first_name__icontains=query)
            )
            qs = qs.filter(or_lookup).distinct()
        return qs


class Projectarticle(models.Model):
    title = models.CharField(max_length=100, verbose_name="Tittel")
    main_content = RichTextUploadingField(blank=True, verbose_name="Brødtekst")
    ingress_content = models.TextField(
        max_length=400,
        blank=True,
        validators=[MaxLengthValidator(400)],
        verbose_name="Ingress",
        help_text="En kort introduksjon til teksten",
    )

    author = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    pub_date = models.DateTimeField("Publication date", default=timezone.now)
    thumbnail = models.ForeignKey(
        Image, on_delete=models.SET_NULL, blank=True, null=True
    )
    redirect = models.IntegerField("Redirect", default=0)

    draft = models.BooleanField(default=False, verbose_name="Utkast")

    objects = ProjectarticleManager()

    def __str__(self):
        return self.title

    @staticmethod
    def get_class():
        return "Projectarticle"

    class Meta:
        app_label = "projectarchive"
        ordering = ("-pub_date",)

    def redirect_id(self):
        if self.redirect:
            return self.redirect
        return self.id


class Upload(models.Model):
    title = models.CharField(max_length=100, verbose_name="Filnavn")
    time = models.DateTimeField(default=timezone.now, verbose_name="Tittel")
    file = models.FileField(upload_to="event-uploads", blank=True)
    number = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        app_label = "projectarchive"

    def save(self, *args, **kwargs):
        # Dersom fjern er huket av i event_edit, slettes hele objektet.
        if self.file == "":
            self.delete()
        else:
            return super(Upload, self).save(*args, **kwargs)
