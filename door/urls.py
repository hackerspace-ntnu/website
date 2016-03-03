from django.conf.urls import url
from .views import door_post

from website.settings import DOOR_KEY

urlpatterns = [
    url(r'^$', door_post, name='door_post'),
]
