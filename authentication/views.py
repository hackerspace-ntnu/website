from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect
from django.utils.http import urlsafe_base64_decode
from django.views.generic import TemplateView, FormView
from django.contrib.auth.tokens import default_token_generator
import requests
from django.contrib.auth.models import User
from userprofile.models import Profile

from django.conf import settings

from oauthlib.oauth2 import WebApplicationClient
from django.contrib.auth import login as auth_login
from django.views import View

dataporten_oauth_client = WebApplicationClient(settings.DATAPORTEN_OAUTH_CLIENT_ID)

def get_callback_redirect_url(request):
    return request.build_absolute_uri(reverse('auth:login_callback'))

class LogoutView(View):
    def get(self, request, *args, **kwargs):
        is_feide_login = request.session.get('feided', False)
        logout(request)
        if is_feide_login:
            return redirect("https://auth.dataporten.no/logout")
        return redirect(reverse('index'))

class LoginView(View):
    def get(self, request, *args, **kwargs):
        dataporten_auth_url = dataporten_oauth_client.prepare_request_uri(
            settings.DATAPORTEN_OAUTH_AUTH_URL,
            redirect_uri=get_callback_redirect_url(request))
        request.session['feided'] = True

        return redirect(dataporten_auth_url)


class LoginCallbackView(View):
    def get(self, request, *args, **kwargs):
        code = self.request.GET.get('code')
        token_request_body = dataporten_oauth_client.prepare_request_body(
            code=code,
            redirect_uri=get_callback_redirect_url(request),
            client_secret=settings.DATAPORTEN_OAUTH_CLIENT_SECRET)

        token_request_response = requests.post(
            settings.DATAPORTEN_OAUTH_TOKEN_URL,
            data=token_request_body,
            headers={
                "content-type": "application/x-www-form-urlencoded",
                "authorization": "Basic {}".format(settings.DATAPORTEN_OAUTH_CLIENT_SECRET),
            })

        if token_request_response.status_code != 200:
            raise Exception("invalid code")

        response_json = token_request_response.json()
        access_token = response_json['access_token']

        # Lag session for bruker
        session = requests.Session()
        session.headers.update({'authorization': 'bearer {}'.format(access_token)})

        user_info = session.get("https://auth.dataporten.no/userinfo").json()
        user_email = user_info['user']['email']
        first_name = " ".join(user_info['user']['name'].split(" ")[0:-1])
        last_name = user_info['user']['name'].split(" ")[-1]
        # Lag catch dersom feidebruker ikke har email. Mest sansynlig testuser.

        try:
            username = user_email.split("@")[0]
        except AttributeError:
            username = first_name + "_testuser_" + last_name 
            user_email = first_name + "-" + last_name + "@hackerspace-ntnu-test.no"

        try:
            # Sjekk om det eksisterer en bruker med denne feide-eposten allerede, og loggi nn
            user = User.objects.get(email=user_email)
            try:
                # Sjekk at bruker har profil
                user.profile
            except Profile.DoesNotExist:
                # Om bruker har bruker, men ikke profil, lag en
                profile = Profile.objects.create(user=user, tos_accepted=False)
        except User.DoesNotExist:
            # Dersom brukeren ikke eksisterer, lag en ny User og Profile objekt
            user = User.objects.create_user(username=username, email=user_email, first_name=first_name, last_name=last_name)
            profile = Profile.objects.create(user=user,  tos_accepted=False)

        # Logg brukeren inn
        auth_login(request, user)
        return redirect('/')
