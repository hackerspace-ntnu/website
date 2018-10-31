from datetime import time, datetime
from django.test import TestCase

# Create your tests here.
from unittest import mock

from internal.models import TimeTable, TimeTableSlotSignup, TimeTableSlot


class TimeTableTest(TestCase):

    def test_create(self):
        TimeTable.create(4, "18H", time(10, 15), 3)
        self.assertEqual(20, TimeTableSlot.objects.all().count())
        self.assertEqual(60, TimeTableSlotSignup.objects.all().count())

    def test_get_time_slot(self):
        TimeTable.create(4, "18H", time(10, 15), 3)
        time_table = TimeTable.objects.get(term="18H")
        self.assertEqual([
            (time(10, 15), time(12, 15)),
            (time(12, 15), time(14, 15)),
            (time(14, 15), time(16, 15)),
            (time(16, 15), time(18, 15))
        ], list(time_table.get_time_slots()))

    @mock.patch("internal.models.datetime")
    def test_get_current_term(self, mocked_datetime):
        mocked_datetime.now.return_value = datetime(2018, 10, 1)
        self.assertEqual("18H", TimeTable.current_term())
        mocked_datetime.now.return_value = datetime(2018, 5, 3)
        self.assertEqual("18V", TimeTable.current_term())
        mocked_datetime.now.return_value = datetime(2000, 12, 31)
        self.assertEqual("00H", TimeTable.current_term())
        mocked_datetime.now.return_value = datetime(2075, 7, 1)
        self.assertEqual("75H", TimeTable.current_term())
        mocked_datetime.now.return_value = datetime(2009, 6, 30)
        self.assertEqual("09V", TimeTable.current_term())

