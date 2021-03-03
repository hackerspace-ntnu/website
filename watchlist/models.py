from django.db import models
from enum import Enum
from datetime import time

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

def generate_shift_slots(shift_length, limit):
    '''
    Generates timeslots for all weekdays
    
    Args:
        shift_length: How many minutes a single shift lasts for.
        limit: The limit on how many people can be registered to a single shift.
    '''
    # Sanity check
    if shift_length < 0 or shift_length > (24*60):
        return

    # We have to remove all existing slots to prevent making duplicates by accident
    for slot in ShiftSlot.objects.all():
        slot.delete()
    
    # Generate and save timeslots
    shifts_per_day = minutes_per_day // shift_length
    for day in Weekdays:
        start = time()
        for slot in range(shifts_per_day):
            end = start + time(minute=shift_length)

            time_slot = ShiftSlot(day)
            time_slot.start = start
            time_slot.end = end
            time_slot.limit = limit
            time_slot.save()

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
            self.start.strftime('HH:MM'),
            self.end.strftime('HH:MM'),
            self.limit
        )

    def validate_limit(self):
        '''Checks that there are <= limit watchers registered to this shift'''
        return self.watchers.count() <= self.limit
