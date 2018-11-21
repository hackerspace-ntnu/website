from django.contrib.auth.decorators import permission_required
from django.urls import path, register_converter

from internal.converters import TermConverter
from internal.views import TimeTableView, SignupView, TimeTableAdminView, TimeTableCreationView

register_converter(TermConverter, "term")

urlpatterns = [
    path("hours", TimeTableView.as_view(), name="hours"),
    path("hours/admin", permission_required("internal.admin_office_hours")(TimeTableAdminView.as_view()), name="admin_hours"),
    path("hours/create", permission_required("internal.admin_office_hours")(TimeTableCreationView.as_view()), name="create_hours"),
    path("hours/<term:term>", TimeTableView.as_view(), name="hours"),
    path("hours/change/<int:pk>", SignupView.as_view(), name="change_hours"),
]
