from django.conf.urls import url
from . import views

from website.settings import DOOR_KEY

urlpatterns = [
    url(r'^$', views.door_post, name='door_post'),
    url(r'^get_status/', views.get_status, name='get_status'),
    url(r'^get_json/', views.get_json, name='get_json'),
    url(r'^door-data/', views.door_data, name='door_data'),
]
