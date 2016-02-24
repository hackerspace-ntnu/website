from django.conf.urls import url
from .views import update_door_status

from website.settings import DOOR_KEY

urlpatterns = [
    url(r'^{}/$'.format(DOOR_KEY), update_door_status, name='door_status'),

]
