# from django.views.generic import TemplateView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.urls import reverse
from django.views.generic import TemplateView, UpdateView, FormView

from internal.forms import TimeTableSignupForm, TimeTableCreationForm
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
            "members": User.objects.filter(groups__name__in=["member"]),
            "time_table": time_table,
        })
        return context_data


class SignupView(PermissionRequiredMixin, UpdateView):
    form_class = TimeTableSignupForm
    model = TimeTableSlotSignup
    permission_required = "internal.change_timetableslotsignup"

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


class TimeTableAdminView(TemplateView):
    template_name = "internal/timetable_admin.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data()
        context_data.update({
            "time_tables": sorted(list(TimeTable.objects.all()), reverse=True)
        })
        return context_data


class TimeTableCreationView(FormView):
    template_name = "internal/timetable_create.html"
    form_class = TimeTableCreationForm

    def get_success_url(self):
        return reverse("admin_hours")

    def form_valid(self, form):
        TimeTable.create(slots=form.cleaned_data["number_of_slots"], term=form.cleaned_data["term"],
                         start_time=form.cleaned_data["start_time"], per_slot=form.cleaned_data["per_slot"])

        return super().form_valid(form)
