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

dataporten_oauth_client = WebApplicationClient(settings.DATAPORTEN_OAUTH_CLIENT_ID)

@login_required
def logout_user(request):
    is_feide_login = request.session.get('feided', False)
    logout(request)
    if is_feide_login:
        return redirect("https://auth.dataporten.no/logout")
    return redirect(reverse('index'))

# Automatically get the user model that is being used by django from its engine
# Feide

def get_callback_redirect_url(request):
    return request.build_absolute_uri(reverse('auth:login_callback'))

def logout(request):
    return redirect("https://auth.dataporten.no/logout")

def make_requests_session(token):
    s = requests.Session()
    s.headers.update({'authorization': 'bearer {}'.format(token)})
    return s

def login(request):
    dataporten_auth_url = dataporten_oauth_client.prepare_request_uri(
        settings.DATAPORTEN_OAUTH_AUTH_URL,
        redirect_uri=get_callback_redirect_url(request))
    request.session['feided'] = True

    return redirect(dataporten_auth_url)


def login_callback(request):
    code = request.GET.get('code')

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
    session = make_requests_session(access_token)

    user_info = session.get("https://auth.dataporten.no/userinfo").json()
    user_email = user_info['user']['email']
    username = user_email.split("@")[0]
    first_name = " ".join(user_info['user']['name'].split(" ")[0:-1])
    last_name = user_info['user']['name'].split(" ")[-1]

    try:
        user = User.objects.get(email=user_email)
        try:
            user.profile
        except Profile.DoesNotExist:
            profile = Profile.objects.create(user=user, tos_accepted=False)
    except User.DoesNotExist:
        user = User.objects.create_user(username=username, email=user_email, first_name=first_name, last_name=last_name)
        profile = Profile.objects.create(user=user,  tos_accepted=False)

    auth_login(request, user)
    return redirect('/')


