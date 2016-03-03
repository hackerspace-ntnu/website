from django.conf.urls import url
from . import views

from website.settings import DOOR_KEY

urlpatterns = [
    url(r'^$', views.door_post, name='door_post'),
    url(r'^get_status/', views.get_status, name='get_status'),
]
