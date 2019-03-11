from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.db import models


class TimeTable(models.Model):
    slots = models.IntegerField()
    term = models.CharField(max_length=3, unique=True)
    start_time = models.TimeField()

    @classmethod
    def create(cls, slots, term, start_time, per_slot=3):
        table = TimeTable(slots=slots, term=term, start_time=start_time)
        table.save()
        for start_time, end_time in table.get_time_slots():
            for day in range(5):
                TimeTableSlot.create(start_time, end_time, day, table, max_number_of_users=per_slot)

    @staticmethod
    def current_term():
        """
        :return: The current term in the format (yy[HV])
        """
        return str(datetime.now().year)[-2:] + "VH"[datetime.now().month > 6]

    def get_time_slots(self):
        """
        :return: A list of time slots (start-, end-time) for a single day in this term
        """
        for time_slot in range(self.slots):
            yield (datetime.combine(datetime.today().date(), self.start_time) + timedelta(hours=2 * time_slot)).time(), \
                  (datetime.combine(datetime.today().date(), self.start_time) + timedelta(
                      hours=2 * (time_slot + 1))).time()

    def __lt__(self, other):
        # Check if the year is different
        if self.term[:2] != other.term[:2]:
            return self.term[:2] < other.term[:2]
        # V is further into the alphabet than H even though the spring term is before the fall term
        return self.term[2] > other.term[2]

    @staticmethod
    def get_users_in_office_now():
        """
        :return: A list of users currently in office
        """
        time_now = datetime.now()

        # The number of current slot may be 0 (outside office hours), 1 (normally), 2 (at the change point)
        current_slot = TimeTableSlot.objects.filter(start_time__lte=time_now.time(), end_time__gte=time_now.time(),
                                                    table__term=TimeTable.current_term(), day=time_now.weekday())
        users = []
        for slot in current_slot:
            # Only care about singup slots where there is actually a user
            users.extend([signup_slot.user for signup_slot in slot.timetableslotsignup_set.filter(user__isnull=False)])

        return users


class TimeTableSlot(models.Model):
    """
    Time table slot for office hours
    """
    start_time = models.TimeField()
    end_time = models.TimeField()
    day = models.IntegerField()
    table = models.ForeignKey(TimeTable, on_delete=models.CASCADE)

    @classmethod
    def create(cls, start_time, end_time, day, table, max_number_of_users=3):
        slot = TimeTableSlot(start_time=start_time, end_time=end_time, day=day, table=table)
        slot.save()
        for signup_slot in range(max_number_of_users):
            TimeTableSlotSignup(time_table_slot=slot).save()


class TimeTableSlotSignup(models.Model):
    """
    A single signup for a time table slot for the office hours
    """
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    time_table_slot = models.ForeignKey(TimeTableSlot, on_delete=models.CASCADE)

    class Meta:
        permissions = (
            ("admin_office_hours", "Can admin office hours"),
        )
