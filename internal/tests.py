from datetime import time, datetime
from django.contrib.auth.models import User, Permission
from django.test import TestCase
# Create your tests here.
from django.urls import reverse
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


class TimeTableSignupViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user("test_user", password="password")
        TimeTable.create(4, "18H", time(10, 15), 3)
        self.add_permission = Permission.objects.get(codename="change_timetableslotsignup")
        self.client.login(username="test_user", password="password")

    def get_slot(self):
        return TimeTableSlotSignup.objects.first()

    def get_signup_url(self):
        return reverse("change_hours", kwargs={"pk": self.get_slot().pk})

    def test_change_allowed(self):
        self.user.user_permissions.add(self.add_permission)
        response = self.client.post(self.get_signup_url(), data={"user": self.user.pk})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.get_slot().user, self.user)

        response = self.client.post(self.get_signup_url(), data={"user": 0})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.get_slot().user, None)

    def test_change_other_no_admin(self):
        self.user.user_permissions.add(self.add_permission)
        user_other = User.objects.create_user("test_other_user")
        user_other.user_permissions.add(self.add_permission)
        slot = self.get_slot()
        slot.user = user_other
        slot.save()
        self.assertEqual(self.get_slot().user, user_other)

        response = self.client.post(self.get_signup_url(), data={"user": self.user.pk})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(self.get_slot().user, user_other)

        response = self.client.post(self.get_signup_url(), data={"user": 0})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(self.get_slot().user, user_other)

    def test_change_without_permission(self):
        response = self.client.post(self.get_signup_url(), data={"user": self.user.pk})
        # Redirect to login page
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.get_slot().user, None)

    def test_change_other_admin(self):
        self.user.user_permissions.add(Permission.objects.get(codename="admin_office_hours"))
        self.user.user_permissions.add(self.add_permission)
        user_other = User.objects.create_user("test_other_user")
        user_other.user_permissions.add(self.add_permission)

        # Check that admins can change to other people
        response = self.client.post(self.get_signup_url(), data={"user": user_other.pk})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.get_slot().user, user_other)

        # Check that admins can change away from other people
        response = self.client.post(self.get_signup_url(), data={"user": self.user.pk})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.get_slot().user, self.user)

    def test_signup_two_slots(self):
        self.user.user_permissions.add(self.add_permission)
        user_other = User.objects.create_user("test_other_user")

        slot = TimeTableSlotSignup.objects.all()[1]
        slot.user = user_other
        slot.save()

        response = self.client.post(self.get_signup_url(), data={"user": self.user.pk})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.get_slot().user, self.user)
