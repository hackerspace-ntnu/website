from itertools import combinations
from django.test import TestCase
import vaktliste.views as vaktliste


class VaktlisteTestCase(TestCase):
    def setUp(self):
        self.test_get()

    def test_get(self):
        self.vakter_json = vaktliste.hent_vaktliste()
        self.vakter_tuples = vaktliste.hent_vaktliste(output="tuples")
        self.assertNotEqual(len(self.vakter_json), 0)
        self.assertNotEqual(len(self.vakter_tuples), 0)

    def test_filter_one(self):
        result = vaktliste.vakt_filter(persons="Karl", full=False)
        self.assertEqual(len(result), 1)

    def test_filter_two(self):
        result = vaktliste.vakt_filter(persons="Amund", full=False)
        hackers = []
        for day in result:
            for time in result[day]:
                hackers += [hacker for hacker in result[day][time]]
        self.assertEqual(len(hackers), 2)

    def test_filter_days(self):
        for i in range(1, 6):
            for day in combinations(["Mandag", "Tirsdag", "Onsdag", "Torsdag", "Fredag"], i):
                result = vaktliste.vakt_filter(days=",".join(day))
                passed = all([d in day for d in result])
                self.assertTrue(passed)

    def test_filter_weekends(self):
        for day in ["Lørdag", "Søndag"]:
            result = vaktliste.vakt_filter(days=day)
            self.assertEqual(len(result), 0)

    def test_filter_out_of_time(self):
        for time in range(0, 10):
            result = vaktliste.vakt_filter(times=str(time))
            for day in result:
                for timeslot in result[day]:
                    self.assertEqual(timeslot, "10:15 - 12:07")
        for time in range(19, 24):
            result = vaktliste.vakt_filter(times=str(time))
            for day in result:
                for timeslot in result[day]:
                    self.assertEqual(timeslot, "16:07 - 18:00")
