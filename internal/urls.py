from django.urls import path

from internal.views import TimeTableView, SignupView

urlpatterns = [
    path("hours", TimeTableView.as_view(), name="hours"),
    path("hours/change/<int:pk>", SignupView.as_view(), name="change_hours"),
]
