from django.conf.urls import url
from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter

from applications.views.application import ApplicationModelViewSet
from applications.views.template_views import ApplicationInfoView, ApplicationView

api_router = DefaultRouter()
api_router.register("application", ApplicationModelViewSet, basename="application")


app_name = "application"

urlpatterns = [
    url(r"^$", ApplicationInfoView.as_view(), name="application_info"),
    url(r"^application", ApplicationView.as_view(), name="application_form"),
    url(
        r"^success",
        TemplateView.as_view(template_name="applications/application_success.html"),
        name="application_success",
    ),
    path("api/", include(api_router.urls)),
]
