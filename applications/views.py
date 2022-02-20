from django.shortcuts import redirect
from django.views.generic import ListView
from django.views.generic.edit import FormView

from applications.forms import ApplicationForm

from .models import ApplicationGroup, ApplicationPeriod


class ApplicationInfoView(ListView):
    template_name = "applications/application_info.html"
    queryset = ApplicationGroup.objects.all()

    def get_context_data(self, **kwargs):
        period = ApplicationPeriod.objects.filter(name="Opptak").first()
        return {
            **super().get_context_data(**kwargs),
            "group_list": ApplicationGroup.objects.filter(project_group=True),
            "main_list": ApplicationGroup.objects.filter(project_group=False),
            "start_date": period.period_start if period else None,
            "end_date": period.period_end if period else None,
            "period_status": period.status() if period else None,
        }


class ApplicationView(FormView):
    template_name = "applications/application_form.html"
    form_class = ApplicationForm
    success_url = "/opptak/success"

    def form_valid(self, form):
        form.save()  # must save before sending email in order to access group choice priorities
        form.send_email()
        return super(ApplicationView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["group_choices"] = ApplicationGroup.objects.all()
        return context

    def dispatch(self, request, *args, **kwargs):
        period = ApplicationPeriod.objects.filter(name="Opptak").first()
        if not period or not period.is_open():
            return redirect("application:application_info")
        return super(ApplicationView, self).dispatch(request, *args, **kwargs)
