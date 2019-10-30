from django.apps import apps
from django.contrib.auth.models import User, AnonymousUser
from django.test import TestCase, RequestFactory, Client
from authentication.apps import AuthenticationConfig
from social_django.models import UserSocialAuth
from django.contrib.auth import get_user_model

from django.conf import settings
from social_django.compat import reverse
from authentication.views import associate_by_email, save_profile
from social_django.utils import load_strategy, load_backend



class AuthenticationConfigTest(TestCase):
    def test_apps(self):
        self.assertEqual(AuthenticationConfig.name, 'authentication')
        self.assertEqual(apps.get_app_config('authentication').name, 'authentication')



class AssociationTest(TestCase):
    def setUp(self):
        self.testuser = User.objects.create(username='testuser_test', password='12345')
        self.testuser.set_password('hello')
        self.testuser.email = "testuser3@ntnu.no"
        self.testuser.save()

        self.backend = load_backend(strategy=load_strategy(), name='dataporten_feide',
                                    redirect_uri='/')
    def test_logout_view(self):
        client = Client()
        client.login(username='testuser_test', password='hello')

        response = client.get(reverse('auth:logout'))

        self.assertEquals(response.status_code, 302)


    def test_login_assoc_mail(self):

        details = {
            'access_token': '123',
            'expires_in': 2000,
            'fullname': 'Test Lastname',
            'profilephoto': '123',
            'profilephoto_url': '123',
            'scope': 'profile userid userid-feide',
            'token_type': 'Bearer',
            'userid': '123',
            'userid_sec': ['feide:123@ntnu.no'],
            'username': 'testuser@ntnu.no'
        }

        associate = associate_by_email(self.backend, details)

        # No users should be returned becuase none are made yet
        self.assertIsNone(associate)

        # Create user

        self.user = User.objects.create(username='testuser', password='12345')
        self.user.set_password('hello')
        self.user.email = "testuser@ntnu.no"
        self.user.save()

        # is_new bør være
        save_profile(self.backend, self.user, response=details, is_new=True)

        # Etter save profile skal følgende være gyldige:

        self.assertEqual(self.user.first_name, "Test")
        self.assertEqual(self.user.last_name, "Lastname")
        self.assertEqual(self.user.email, "testuser@ntnu.no")
        self.assertIsNotNone(self.user.profile)


        # Bruker bør nå associates med email
        associate = associate_by_email(self.backend, details)
        self.assertIsNotNone(associate)
        self.user.delete()

    def test_login_assoc_studmail(self):
        details = {
            'access_token': '1234',
            'expires_in': 2000,
            'fullname': 'Old Studuser',
            'profilephoto': '1234',
            'profilephoto_url': '1234',
            'scope': 'profile userid userid-feide',
            'token_type': 'Bearer',
            'userid': '333',
            'userid_sec': ['feide:1234@ntnu.no'],
            'username': 'testuser2@ntnu.no'
        }

        # Create user with old studmail

        self.user = User.objects.create(username='testuser2', password='12345')
        self.user.set_password('hello')
        self.user.email = "testuser2@stud.ntnu.no"
        self.user.save()

        # Først skal mailen være gammel
        self.assertEqual(self.user.email, "testuser2@stud.ntnu.no")

        save_profile(self.backend, self.user, response=details, is_new=True)

        associate = associate_by_email(self.backend, details)

        # Etter association skal den returnere at den fant en bruker
        self.assertIsNotNone(associate)
        # Deretter skal mailen oppdateres
        self.assertEqual(self.user.email, "testuser2@ntnu.no")
        self.user.delete()

    def test_existing_user_profiles(self):
        self.user = User.objects.create(username='testuser2', password='12345')
        self.user.set_password('hello')
        self.user.email = "testuser2@stud.ntnu.no"
        self.user.save()


        # Test existing user without profile
        save_profile(self.backend, self.user, response={}, is_new=False)
        self.assertIsNotNone(self.user.profile)

        # Test existing user with profile
        save_profile(self.backend, self.user, response={}, is_new=False)
        self.assertIsNotNone(self.user.profile)

    def test_assoc_existing_user(self):
        associate = associate_by_email(self.backend, {}, user=self.testuser)
        self.assertIsNone(associate)





