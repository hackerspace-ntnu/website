from django.urls import path
from django.views.generic import TemplateView

from applications import views

app_name = "application"

urlpatterns = [
    path("", views.ApplicationInfoView.as_view(), name="application_info"),
    path("application/", views.ApplicationView.as_view(), name="application_form"),
    path(
        "success/",
        TemplateView.as_view(template_name="applications/application_success.html"),
        name="application_success",
    ),
]
