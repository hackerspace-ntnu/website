import project
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView, ListView, UpdateView, CreateView, DeleteView
from .models import Project
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin





# Detail av project
class ProjectView(DetailView):
    model = Project
    template_name = "project/project_detail.html"


# lager nytt prosjekt i arkivet
class ProjectCreateView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Project
    template_name = "project/create_project.html"
    # success_url = "/events/"
    permission_required = 'project.add_project'            # Se på dette senere for permission til arkivet

    def get_success_message(self, cleaned_data):
        return "Prosjekt er opprettet og publisert"

    def get_success_url(self):
        return reverse('projects:details', kwargs={'pk': self.object.id})

    # def get_context_data(self, **kwargs):
    #     context = super(ProjectCreateView, self).get_context_data(**kwargs)
    #     if self.request.POST:
    #         context['uploads_form'] = uploadformset(self.request.POST, self.request.FILES)
    #     else:
    #         context['uploads_form'] = uploadformset(instance=self.object)
    #     return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        self.object = form.save(commit=False)
        context = self.get_context_data()

        upload_form = context['uploads_form']

        if upload_form.is_valid():
            self.object = form.save()
            upload_form.instance = self.object
            upload_form.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))


# Viser ting som liste
class ProjectListView(ListView):
    model = Project
    template_name = "project/project_list.html"
    paginate_by = 10








