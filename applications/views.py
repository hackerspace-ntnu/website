from datetime import datetime

from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import FormView

from applications.forms import ApplicationForm

from .models import ApplicationGroup, ApplicationPeriod


class ApplicationInfoView(ListView):
    template_name = "applications/application_info.html"
    queryset = ApplicationGroup.objects.all()

    def get_context_data(self, **kwargs):
        context = super(ApplicationInfoView, self).get_context_data(**kwargs)
        context["group_list"] = ApplicationGroup.objects.filter(project_group=True)
        context["main_list"] = ApplicationGroup.objects.filter(project_group=False)

        return context


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
        current_date = datetime.now()
        if not ApplicationPeriod.objects.filter(name="Opptak"):
            ap = ApplicationPeriod.objects.create(
                name="Opptak",
                period_start=datetime(2018, 1, 1),
                period_end=datetime(2018, 1, 2),
            ).save()

        start_date = ApplicationPeriod.objects.get(name="Opptak").period_start
        end_date = ApplicationPeriod.objects.get(name="Opptak").period_end
        context = {"start_date": start_date, "end_date": end_date}

        if current_date < start_date:
            return render(
                request, "applications/application_too_early.html", context=context
            )
        elif current_date > end_date:
            return render(
                request, "applications/application_too_late.html", context=context
            )
        else:
            return super(ApplicationView, self).dispatch(request, *args, **kwargs)
