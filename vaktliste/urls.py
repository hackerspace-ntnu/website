from django.conf.urls import url
from . import views


app_name = 'vaktliste'

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^filter$', views.vakter, name="filter"),
    url(r'^current$', views.current, name="Nå"),
]
