from django.conf.urls import url
from applications import views

urlpatterns = [
    url(r'^$', views.no_application, name='no_application'),
    #url(r'^$', views.project_application_form, name='project_application_form'),
    #url(r'^others/$', views.application_form, name='application_form'),
    #url(r'^done/$', views.application_sent, name="application_sent")
]
