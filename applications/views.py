from django.views.generic import ListView
from django.views.generic.edit import FormView

from applications.forms import ApplicationForm

from .models import ApplicationGroup


class ApplicationInfoView(ListView):
    template_name = "applications/application_info.html"
    queryset = ApplicationGroup.objects.all()

    def get_context_data(self, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            "group_list": ApplicationGroup.objects.filter(
                project_group=True, open_for_applications=True
            ),
            "main_list": ApplicationGroup.objects.filter(
                project_group=False, open_for_applications=True
            ),
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
