from django.shortcuts import render
from applications.forms import ApplicationForm
from datetime import datetime
from django.views.generic.edit import FormView


APPLICATION_START_DATE = datetime(2018, 8, 13)
APPLICATION_END_DATE = datetime(2018, 9, 3)


class ApplicationView(FormView):
    template_name = 'applications/application_form.html'
    form_class = ApplicationForm
    success_url = '/opptak/success'

    def form_valid(self, form):
        form.send_email()
        form.save()
        return super(ApplicationView, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        current_date = datetime.now()
        if current_date < APPLICATION_START_DATE:
            return render(request, 'applications/application_too_early.html')
        elif current_date > APPLICATION_END_DATE:
            return render(request, 'applications/application_too_late.html')
        else:
            return super(ApplicationView, self).dispatch(request, *args, **kwargs)
