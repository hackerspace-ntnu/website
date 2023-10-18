from django.urls import path

from . import views

app_name = "internalportal"

urlpatterns = [
    path("", views.InternalPortalView.as_view(), name="internalportal"),
    path("applications/", views.ApplicationsView.as_view(), name="applications"),
    path("applications/<int:pk>", views.ApplicationView.as_view(), name="application"),
]
