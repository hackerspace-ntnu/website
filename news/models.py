from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone
from django.contrib.auth.admin import User
from files.models import Image


class Article(models.Model):
    title = models.CharField(max_length=100, verbose_name='Title')
    main_content = RichTextUploadingField(blank=True)
    ingress_content = models.CharField(max_length=300, blank=True)

    author = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    internal = models.BooleanField(default=False, verbose_name='Intern')
    pub_date = models.DateTimeField('Publication date', default=timezone.now)
    thumbnail = models.ForeignKey(Image, on_delete=models.SET_NULL, blank=True, null=True)
    redirect = models.IntegerField('Redirect', default=0)

    draft = models.BooleanField(default=False, verbose_name='Utkast')

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
    ingress_content = models.CharField(max_length=300, blank=True, verbose_name='Ingress', help_text="En kort setning om hva artikkelen inneholder")
    pub_date = models.DateTimeField(default=timezone.now, verbose_name='Publiseringsdato')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    responsible = models.ForeignKey(User, related_name="responsible", on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Arrangementansvarlig")

    thumbnail = models.ForeignKey(Image, on_delete=models.SET_NULL, blank=True, null=True)

    internal = models.BooleanField(default=False, verbose_name='Intern')
    registration = models.BooleanField(default=False, verbose_name='Påmelding')
    max_limit = models.PositiveIntegerField(blank=True, null=True, default=0, verbose_name='Maks påmeldte')
    registration_start = models.DateTimeField(default=timezone.now, verbose_name='Påmeldingsstart')
    registration_end = models.DateTimeField(default=timezone.now, verbose_name='Påmeldingsfrist')
    deregistration_end = models.DateTimeField(default=timezone.now, verbose_name='Avmeldingsfrist')
    external_registration = models.CharField(blank=True, max_length=200, default='', verbose_name='Lenke for ekstern påmelding')

    time_start = models.DateTimeField(verbose_name='Starttidspunkt', null=True)
    time_end = models.DateTimeField(verbose_name='Sluttidspunkt', null=True)

    servering = models.BooleanField(default=False)
    place = models.CharField(max_length=100, blank=True, verbose_name='Sted')
    place_href = models.CharField(max_length=200, blank=True, verbose_name='Sted URL')


    @property
    def can_register(self):
        if self.registration_start < timezone.now() < self.registration_end:
            return "ok"
        elif timezone.now() < self.registration_start:
            return "tidlig"
        return "sen"

    @property
    def can_deregister(self):
        if timezone.now() < self.deregistration_end:
            return True
        return False

    @property
    def expired(self):
        if self.time_end < timezone.now():
            return True
        return False

    @property
    def is_past_start(self):
        return self.time_start < timezone.now()

    @property
    def is_past_due(self):
        '''
            Denne brukes i regroup og tallene strippes vekk, kun brukt for
            dictsort i regroup.
        '''
        if self.time_start < timezone.now() < self.time_end:
            return "1 Pågående arrangementer"
        if self.time_end > timezone.now():
            return "2 Kommende arrangementer"
        else:
            return "3 Tidligere arrangementer"

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

    def get_food_preferences_of_registered(self):

        preferences = []

        for reg in self.registration_list():
            profile = reg.user.profile
            if profile.has_food_preferences():
                preferences.append(profile.get_food_preferences())

        return preferences

    def get_allergies_count(self):

        count = {
            'glutenfritt': 0,
            'vegetar': 0,
            'vegan': 0
        }

        for reg in self.registration_list():
            if reg.user.profile.allergi_gluten:
                count['glutenfritt'] += 1
            if reg.user.profile.allergi_vegetar:
                count['vegetar'] += 1
            if reg.user.profile.allergi_vegan:
                count['vegan'] += 1

        return count

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
    file = models.FileField(upload_to='event-uploads', blank=True)
    number = models.IntegerField(default=0)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="files")

    def __str__(self):
        return self.title

    class Meta:
        app_label = 'news'

    def save(self, *args, **kwargs):
        # Dersom fjern er huket av i event_edit, slettes hele objektet.
        if self.file ==  "":
            self.delete()
        else:
            return super(Upload, self).save(*args, **kwargs)


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
        return EventRegistration.get_registrations(event).order_by('date')[event.max_limit:]

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
