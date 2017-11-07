from django.conf.urls import url
from . import views


app_name = 'vaktliste'

urlpatterns = [
    url(r'^$', views.vakter, name="index"),
    url(r'^current$', views.current, name="Nå"),
]
