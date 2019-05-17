from django.conf.urls import url
from django.views.generic import TemplateView
from applications import views

app_name = 'application'

urlpatterns = [
    url(r'^$', views.ApplicationInfoView.as_view(), name='application_info'),
    url(r'^application', views.ApplicationView.as_view(), name='application_form'),
    url(r'^success', TemplateView.as_view(template_name="applications/application_success.html"), name='application_success'),
]
