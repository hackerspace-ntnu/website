from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone
from django.contrib.auth.admin import User
from files.models import Image
import re

class Article(models.Model):
    title = models.CharField(max_length=100, verbose_name='Title')
    main_content = RichTextUploadingField(blank=True)
    ingress_content = models.CharField(max_length=300, blank=True)

    internal = models.BooleanField(default=False, verbose_name='Intern')
    pub_date = models.DateTimeField('Publication date', default=timezone.now)
    thumbnail = models.ForeignKey(Image, on_delete=models.SET_NULL, blank=True, null=True)
    redirect = models.IntegerField('Redirect', default=0)

    def __str__(self):
        return self.title

    @staticmethod
    def get_class():
        return "Article"

    class Meta:
        app_label = 'news'
        ordering = ('-pub_date',)
        permissions = (
                ("can_view_internal_article", "Can see internal articles"),
                )

    def redirect_id(self):
        if self.redirect:
            return self.redirect
        return self.id


class Event(models.Model):
    title = models.CharField(max_length=100, verbose_name='Tittel')
    main_content = RichTextUploadingField(blank=True, verbose_name='Artikkel')
    ingress_content = models.CharField(max_length=300, blank=True, verbose_name='Ingress')
    pub_date = models.DateTimeField(default=timezone.now, verbose_name='Publiseringsdato')
    thumbnail = models.ForeignKey(Image, on_delete=models.SET_NULL, blank=True, null=True, )

    internal = models.BooleanField(default=False, verbose_name='Intern')
    registration = models.BooleanField(default=False, verbose_name='Påmelding')
    max_limit = models.PositiveIntegerField(blank=True, null=True, default=0, verbose_name='Max påmeldte')
    registration_start = models.DateTimeField(default=timezone.now, verbose_name='Registrering start')
    deregistration_end = models.DateTimeField(default=timezone.now, verbose_name='Avregistrering slutt')
    external_registration = models.CharField(blank=True, max_length=200, default='', verbose_name='Lenke for ekstern påmelding')

    time_start = models.DateTimeField(verbose_name='Start tidspunkt')
    time_end = models.DateTimeField(verbose_name='Slutt tidspunkt')
    servering = models.BooleanField(default=False)
    place = models.CharField(max_length=100, blank=True, verbose_name='Sted')
    place_href = models.CharField(max_length=200, blank=True, verbose_name='Sted URL')

    def __str__(self):
        return self.title

    def registered_count(self):
        '''
        Finds the number of registered users not in the waiting list for the event.

        :return: The number of registered users for the event, excluding waitlisted
        '''
        return len(EventRegistration.get_registrations(self)) - len(EventRegistration.get_waitlist(self))

    def waiting_count(self):
        '''
        Finds the number of waitlisted users for the event. Does not count any user that is in
        the normal list for the event.

        :return: The number of registered users for the event
        '''
        return len(EventRegistration.get_waitlist(self))

    def is_registered(self, user):
        '''
        Check if the user is registered for the event and not on the waiting list

        :param user: The user to check
        :return: A boolean indicating if the user is registered for the event
        '''
        return user in [registration.user for registration in
                        EventRegistration.get_registrations(self)]


    def is_waiting(self, user):
        '''
        Checks if the user is registered for the event and on the waiting list

        :param user: The user to check
        :return: A boolean indicating if the user is on the waiting list
        '''
        return user in [registration.user for registration in EventRegistration.get_waitlist(self)]

    def userstatus(self, user):
        '''
        Finds the registration status of the user

        :param user: The user to get registration status for
        :return: A string representing the user status
        '''
        if self.is_waiting(user):
            return "på ventelisten"
        if self.is_registered(user):
            return "påmeldt"
        return "ikke påmeldt"

    def get_position(self, user):
        '''
        Retreives the position in waitlist for a given event

        eparam event: The event to retrieve the waitlist for
        :return: The waitlist
        '''
        return self.wait_list().index(user) + 1

    def registered_percentage(self):
        '''
        Finds the percentage of the slots taken. If limit is 0, return 100% instead

        :return: Percentage of slots taken
        '''
        if self.max_limit:
            return round(self.registered_count() / self.max_limit * 100)
        else:
            return 100

    def get_allergies_registered(self):
        user_list = self.registered_list()
        gluten_count = 0
        vegetar_count = 0
        vegan_count = 0
        annet_list = []


        for user in user_list:
            if user.profile.allergi_gluten:
                gluten_count += 1
            if user.profile.allergi_vegetar:
                vegetar_count += 1
            if user.profile.allergi_vegan:
                vegan_count += 1
            if user.profile.allergi_annet:
                annet_list.append(user.profile.allergi_annet)

        result = {
                'gluten': gluten_count,
                'vegetar': vegetar_count,
                'vegan': vegan_count,
                'annet': annet_list
                }
        return result

    def registered_list(self):
        '''
        Create a list of the registered users for the event

        :return: A list of the registered users for the event
        '''
        return [registration.user for registration in EventRegistration.get_registrations(self)]

    def registration_list(self):
        '''
        Create a list of the registered users for the event

        :return: A list of the registered users for the event
        '''
        return [registration for registration in EventRegistration.get_registrations(self)]

    def wait_list(self):
        '''
        Creates a list containing the full name and priority of the users in the waiting list

        :return: Simplified waiting list
        '''
        return [registration.user for registration in EventRegistration.get_waitlist(self)]

    def can_edit_registration_status(self, user):
        '''
        Checks if the given user can change their registration status

        :param user: The user to check
        :return: A boolean indicating if the user can change their registration status
        '''
        if self.is_registered(user) or self.is_waiting(user):
            return timezone.now() < self.deregistration_end
        return self.registration_start < timezone.now() < self.time_end

    class Meta:
        app_label = 'news'
        ordering = ("time_start",)
        permissions = (
                ("can_see_attendees", "Can see attending, waitlist, register meetup in a event"),
                ("can_view_internal_event", "Can see internal events"),
                )


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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="registrations")
    date = models.DateTimeField(default=timezone.now, verbose_name="Registration time")
    attended = models.BooleanField(default=False)


    @staticmethod
    def get_waitlist(event):
        '''
        Retreives the waitlist for a given event

        :param event: The event to retrieve the waitlist for
        :return: The waitlist
        '''
        return EventRegistration.get_ordered_event_registrations(event)[event.max_limit:]

    @staticmethod
    def get_ordered_event_registrations(event):
        '''
        Retrieves all event registrations for a given event ordered by date

        :param event: The event to get event registrations for
        :return: A queryset of all event registration for the event ordered by date
        '''
        return EventRegistration.get_registrations(event).order_by('date')


    @staticmethod
    def get_registrations(event):
        '''
        Retrieves all registrations for a given event

        :param event: The event to get registrations for
        :return: A list of all registrations for an event
        '''
        return EventRegistration.objects.filter(event=event)


    def username(self):
        return self.user.username

    def is_waitlisted(self):
        '''
        Retreives the waitlist for a given event

        :param event: The event to retrieve the waitlist for
        :return: The waitlist
        '''
        return self.event.is_waiting(self.user)
