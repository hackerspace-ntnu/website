from django.conf.urls import url
from applications import views

urlpatterns = [
    url(r'^$', views.application_form, name='application_form'),
    url(r'^done/$', views.application_sent, name="application_sent")
]
