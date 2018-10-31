# from django.views.generic import TemplateView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.views.generic import TemplateView, UpdateView

from internal.forms import TimeTableSignupForm
from internal.models import TimeTable, TimeTableSlot, TimeTableSlotSignup


class TimeTableView(TemplateView):
    template_name = "internal/timetable.html"

    def get_context_data(self, term=TimeTable.current_term(), **kwargs):
        context_data = super().get_context_data(**kwargs)

        time_table = TimeTable.objects.get(term=term)

        context_data.update({
            "slots": [{
                "start_time": start_time, "end_time": end_time,
                "days": [
                    [*time_table_slot.timetableslotsignup_set.all()]
                    for time_table_slot in
                    TimeTableSlot.objects.filter(table=time_table, start_time=start_time).order_by("day")
                ]
            } for start_time, end_time in time_table.get_time_slots()
            ],
            "members": User.objects.filter(groups__name__in=["member"])
        })
        return context_data


class SignupView(PermissionRequiredMixin, UpdateView):
    form_class = TimeTableSignupForm
    model = TimeTableSlotSignup
    permission_required = "internal.change_timetableslotsignup"
    # No redirection

    def form_valid(self, form):
        prior_user = TimeTableSlotSignup.objects.get(pk=self.object.pk).user
        current_user = self.object.user
        if prior_user is not None and prior_user != self.request.user and not self.request.user.has_perm(
                "internal.admin_office_hours"):
            # Check if the user is allowed to change the given signup field
            return HttpResponseForbidden()

        if current_user not in [None, self.request.user] and not self.request.user.has_perm(
                "internal.admin_office_hours"):
            # Check if the user can assign the given user to the give signup field
            return HttpResponseForbidden()

        self.object.save()
        return HttpResponse("")

    def form_invalid(self, form):
        return HttpResponseBadRequest()
