from django.conf.urls import url
from django.views.generic import TemplateView

from applications.views.application import ApplicationModelViewSet
from applications.views.template_views import ApplicationInfoView, ApplicationView
from website.urls import api_router

api_router.register("applications", ApplicationModelViewSet, basename="applications")


app_name = "application"

urlpatterns = [
    url(r"^$", ApplicationInfoView.as_view(), name="application_info"),
    url(r"^application", ApplicationView.as_view(), name="application_form"),
    url(
        r"^success",
        TemplateView.as_view(template_name="applications/application_success.html"),
        name="application_success",
    ),
]
