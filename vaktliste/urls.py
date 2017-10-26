from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.vakter, name="index"),
    url(r'^personsok$', views.personsok, name="personsok")
]
