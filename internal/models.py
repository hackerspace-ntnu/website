from django.contrib.auth.models import User
from django.db import models


class TimeTableSlot(models.Model):
    """
    Time table slot for office hours
    """
    start_time = models.TimeField()
    end_time = models.TimeField()
    day = models.IntegerField()
    term = models.CharField(max_length=20)

    @classmethod
    def create(cls, start_time, end_time, day, term, max_number_of_users=3):
        slot = TimeTableSlot(start_time=start_time, end_time=end_time, term=term, day=day)
        slot.save()
        for signup_slot in range(max_number_of_users):
            TimeTableSlotSignup(time_table_slot=slot).save()


class TimeTableSlotSignup(models.Model):
    """
    A single signup for a time table slot for the office hours
    """
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    time_table_slot = models.ForeignKey(TimeTableSlot, on_delete=models.CASCADE)
