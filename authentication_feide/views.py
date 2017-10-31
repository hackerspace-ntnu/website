from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from django.urls import reverse

from .models import UserModel

from oauthlib.oauth2 import WebApplicationClient

import requests

dataporten_oauth_client = WebApplicationClient(settings.DATAPORTEN_OAUTH_CLIENT_ID)

def get_callback_redirect_url(request):
    return request.build_absolute_uri(reverse(login_callback))

def make_requests_session(token):
    s = requests.Session()
    s.headers.update({'authorization': 'bearer {}'.format(token)})
    return s

# Create your views here.

def index(request):
    return HttpResponse("nothing")

def login(request):
    dataporten_auth_url = dataporten_oauth_client.prepare_request_uri(
            settings.DATAPORTEN_OAUTH_AUTH_URL, 
            redirect_uri=get_callback_redirect_url(request))

    context = {
        "auth_url": dataporten_auth_url,
    }
    return render(request, 'login.html', context=context)

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
    session = make_requests_session(response_json['access_token'])

    print(session.get("https://auth.dataporten.no/userinfo").json())

    return HttpResponse("success")
