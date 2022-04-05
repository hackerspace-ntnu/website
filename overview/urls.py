from django.urls import path

from . import views

app_name = "overview"

urlpatterns = [
    path("", views.OverviewView.as_view(), name="overview"),
]
