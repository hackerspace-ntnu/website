from django.apps import apps
from django.urls import reverse
from django.test import TestCase, Client
from applications.models import ApplicationPeriod, ApplicationGroup
from applications.apps import ApplicationsConfig
from applications.forms import ApplicationForm
from django.core import mail


from applications.validators import validate_phone_number
from django.core.exceptions import ValidationError


class ApplicationsConfigTest(TestCase):
    def test_apps(self):
        self.assertEqual(ApplicationsConfig.name, "applications")
        self.assertEqual(apps.get_app_config("applications").name, "applications")


class ApplicationValidatorTest(TestCase):
    def test_phone_validator(self):

        with self.assertRaises(ValidationError):
            # Too long
            response = validate_phone_number("123123121")

        with self.assertRaises(ValidationError):
            # No digit
            response = validate_phone_number("123123121asd")


class ApplicationInfoViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.response = self.client.get(reverse("application:application_info"))

    def test_context(self):
        self.assertIsNotNone(self.response.context["group_list"])
        self.assertIsNotNone(self.response.context["main_list"])


class ApplicationFormViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.response = self.client.get(reverse("application:application_form"))

    def test_context(self):
        self.assertIsNotNone(self.response.context["start_date"])
        self.assertIsNotNone(self.response.context["end_date"])

    def test_forms(self):

        ApplicationGroup.objects.create(name="DevOps", text_main="asd")

        ApplicationGroup.objects.create(name="LabOps", text_main="asd")

        data = {
            "name": "Testesson Test",
            "email": "blabb@blab.no",
            "phone": "12312312",
            "study": "informatikk",
            "year": 2,
            "group_choice": "1,2",
            "knowledge_of_hs": "blabla",
            "about": "blabla",
            "application_text": "blabla",
        }

        self.form = ApplicationForm(data)
        self.form.save()
        self.form.send_email()

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(
            mail.outbox[0].subject, "[Hackerspace NTNU] Søknad er registrert!"
        )
        self.assertEqual(mail.outbox[0].to[0], data.get("email"))
        self.assertEqual(
            mail.outbox[0].body,
            """Hei Testesson Test!

Dette er en bekreftelse på at din søknad er registrert.

Du har søkt følgende grupper:

1. DevOps

2. LabOps


Vi svarer på søknader fortløpende etter søknadsfristen går ut.
Denne mailen kan ikke besvares.

Dersom du skulle ha noen spørsmål vedrørende din søknad, ta kontakt med
hackerspace-styret@idi.ntnu.no


Tusen takk for din interesse. :-)


Mvh,
Styret i Hackerspace NTNU
""",
        )
