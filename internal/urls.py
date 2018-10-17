from django.urls import path

from internal.views import TimeTableView, SignupView

urlpatterns = [
    path("hours", TimeTableView.as_view()),
    path("hours/change/<int:pk>", SignupView.as_view()),
]
