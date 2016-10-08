from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone
from django.contrib.auth.admin import User
from files.models import Image


class Article(models.Model):
    title = models.CharField(max_length=100, verbose_name='Title')
    main_content = RichTextUploadingField(blank=True)
    ingress_content = RichTextUploadingField(blank=True)

    pub_date = models.DateTimeField('Publication date', default=timezone.now)
    thumbnail = models.ForeignKey(Image, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.title

    @staticmethod
    def get_class():
        return "Article"

    class Meta:
        app_label = 'news'
        ordering = ('-pub_date',)


class Event(models.Model):
    title = models.CharField(max_length=100, verbose_name='Title')
    main_content = RichTextUploadingField(blank=True)
    ingress_content = RichTextUploadingField(blank=True)
    pub_date = models.DateTimeField('Publication date', default=timezone.now)
    thumbnail = models.ForeignKey(Image, on_delete=models.SET_NULL, blank=True, null=True)

    registration = models.BooleanField(default=False)
    max_limit = models.PositiveIntegerField(blank=True, null=True, default=0)
    registration_datetime = models.DateTimeField('Registration opening date', default=timezone.now)

    time_start = models.DateTimeField('Start time')
    time_end = models.DateTimeField('End time')
    place = models.CharField(max_length=100, verbose_name='Place', blank=True)
    place_href = models.CharField(max_length=200, verbose_name='Place URL', blank=True)

    def __str__(self):
        return self.title

    @staticmethod
    def get_class():
        return "Event"

    def registered_count(self):
        return min(self.max_limit, len(EventRegistration.objects.filter(event=self)))

    def is_registered(self, user):
        if user in [er.user for er in EventRegistration.objects.filter(event=self).order_by('date')][:self.max_limit]:
            return True
        return False

    def is_waiting(self, user):
        if user in [er.user for er in EventRegistration.objects.filter(event=self).order_by('date')][self.max_limit:]:
            return True
        return False

    def userstatus(self, user):
        if self.is_registered(user): return "Påmeldt"
        if self.is_waiting(user): return "Ventelista"
        return "Ikke påmeldt"

    def registered_percentage(self):
        return round(self.registered_count() / self.max_limit * 100)

    def registered_list(self):
        return ["%s %s" % (er.user.first_name, er.user.last_name) for er in EventRegistration.objects.filter(event=self).order_by('date')][:self.max_limit]

    def wait_list(self):
        return ["%s %s" % (er.user.first_name, er.user.last_name) for er in EventRegistration.objects.filter(event=self).order_by('date')][self.max_limit:]

    class Meta:
        app_label = 'news'
        ordering = ("-time_start",)


class Upload(models.Model):
    title = models.CharField(max_length=100, verbose_name='Filnavn')
    time = models.DateTimeField(default=timezone.now, verbose_name='Tittel')
    file = models.FileField(upload_to='uploads')
    number = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        app_label = 'news'


class EventRegistration(models.Model):
    user = models.ForeignKey(User)
    event = models.ForeignKey(Event)
    date = models.DateTimeField(default=timezone.now, verbose_name="Registration time")

    def username(self):
        return self.user.username

    def __str__(self):
        return "%s %s" % (self.user.first_name, self.user.last_name)
