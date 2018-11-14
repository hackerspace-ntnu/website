from django.urls import path, register_converter

from internal.converters import TermConverter
from internal.views import TimeTableView, SignupView

register_converter(TermConverter, "term")

urlpatterns = [
    path("hours", TimeTableView.as_view(), name="hours"),
    path("hours/<term:term>", TimeTableView.as_view(), name="hours"),
    path("hours/change/<int:pk>", SignupView.as_view(), name="change_hours"),
]
