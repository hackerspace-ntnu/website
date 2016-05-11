from django.conf.urls import url
from applications import views

urlpatterns = [
    url(r'^$', views.application_form, name='application_form'),
]
