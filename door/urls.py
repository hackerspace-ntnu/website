from django.urls import path

from . import views

urlpatterns = [
    path("", views.DoorView.as_view(), name="door_post"),
    path("json", views.DoorJsonView.as_view(), name="get_json"),
]
