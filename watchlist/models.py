from django.db import models
from enum import Enum
from datetime import time, timedelta

from django.contrib.auth.models import User

class Weekdays(Enum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6
weekday_loc = ['Mandag', 'Tirsdag', 'Onsdag', 'Torsdag', 'Fredag', 'Lørdag', 'Søndag']

def generate_watchlist(shift_length, day_start, day_end, limit):
    '''
    Generates timeslots for all weekdays
    
    Args:
        shift_length: How many minutes a single shift lasts for.
        day_start: A timedelta object describing when the first shift starts.
        day_end: A timedelta object describing when the last shift ends.
        limit: The limit on how many people can be registered to a single shift.
    '''
    # Sanity check
    if shift_length < 0 or shift_length > (24*60):
        return

    # We have to remove all existing slots to prevent making duplicates by accident
    for slot in ShiftSlot.objects.all():
        slot.delete()
    
    # Generate and save timeslots
    shifts_per_day = ((day_end - day_start).seconds // 60) // shift_length
    for day in Weekdays:
        start = day_start
        for slot in range(shifts_per_day):
            end = start + timedelta(minutes=shift_length)

            time_slot = ShiftSlot(
                weekday=day.value,
                # whoever wrote the datetime module is an idiot
                start=time(hour=(start.seconds // 3600), minute=(start.seconds // 60)%60),
                end=time(hour=(end.seconds // 3600), minute=(end.seconds // 60)%60),
                limit=limit
            )
            time_slot.save()

            start = end

class ShiftSlot(models.Model):
    # Which day of the week does this slot belong to
    weekday = models.IntegerField('Ukedag', null=False)
    # Time of day when the shift starts
    start = models.TimeField('Starttid', null=False)
    # Time of day when the shift ends
    end = models.TimeField('Sluttid', null=False)
    # Who's taking this shift?
    watchers = models.ManyToManyField(User, 'watches', verbose_name='Vaktansvarlige')

    # How many can register for this shift
    limit = models.IntegerField('Antallsbegrensing', null=False, blank=False)

    def __str__(self):
        return "{} - {}-{} (x{})".format(
            weekday_loc[self.weekday],
            self.start.strftime('%H:%M'),
            self.end.strftime('%H:%M'),
            self.limit
        )

    def validate_limit(self):
        '''Checks that there are <= limit watchers registered to this shift'''
        return self.watchers.count() <= self.limit
