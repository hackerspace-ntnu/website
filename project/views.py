from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView, ListView, UpdateView, CreateView, DeleteView
from .forms import ProjectForm
from .models import Project

from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages


# Detail av project
class ProjectView(DetailView):
    model = Project
    template_name = "project/project_detail.html"

    def dispatch(self, request, *args, **kwargs):

        project = self.get_object()

        # If the article is a draft, check if user is the author
        if project.draft and not request.user == project.author:

            # Stores log-in prompt message to be displayed with redirect request
            messages.add_message(request, messages.WARNING, 'Du har ikke tilgang til artikkelen')

            return redirect("/")

        return super(ProjectView, self).dispatch(request, *args, **kwargs)





# lager nytt prosjekt i arkivet
class ProjectCreateView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'project/edit_project.html'
    permission_required = 'project.add_project'            # Se på dette senere for permission til arkivet

    def get_success_message(self, cleaned_data):
        if self.object.draft:
            return "Prosjektet er opprettet som utkast"
        return "Prosjektet er opprettet og publisert"

    def get_success_url(self):
        return reverse('project:details', kwargs={'pk': self.object.id})

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)



# ----------------------------------------------------------------------------------
# Viser ting som liste
class ProjectListView(ListView):
    model = Project
    template_name = "project/project_list.html"
    paginate_by = 10

    def get_queryset(self):
        # Retrieve published articles (so no drafts)
        projects = Project.objects.order_by('-pub_date').filter(draft=False)
        return projects
        # return projects.filter(internal=False)

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        # context['indicator_text'] = self.get_internal_articles_indicator()

        # Retrieve any user drafts if logged in
        if self.request.user.has_perm("project.add_article"):
            context['drafts'] = Project.objects.order_by('-pub_date').filter(author=self.request.user,draft=True)

        return context
# ----------------------------------------------------------------------------------


class ProjectUpdateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = "project/edit_project.html"
    permission_required = "project.change_article"
    success_message = "Prosjektartikkelen er oppdatert."

    def get_success_url(self):
        return reverse('project:details', kwargs={'pk': self.object.id})



class ProjectDeleteView(PermissionRequiredMixin, DeleteView):
    model = Project
    success_url = "/project/"
    permission_required = "project.delete_article"





# from django.shortcuts import get_object_or_404, redirect
# from django.views.generic import DetailView, ListView, UpdateView, CreateView, DeleteView
# from .forms import uploadformset, ProjectForm
# from .models import Project
# from django.contrib.auth.decorators import login_required
# from django.urls import reverse
# from django.http import HttpResponseRedirect
# from django.contrib.auth.mixins import PermissionRequiredMixin
# from django.contrib.messages.views import SuccessMessageMixin
# from django.contrib import messages
# from datetime import datetime, timedelta


# # Detail av project
# class ProjectView(DetailView):
#     model = Project
#     template_name = "project/project_detail.html"

#     def dispatch(self, request, *args, **kwargs):

#         project = self.get_object()

#         # If the article is a draft, check if user is the author
#         if project.draft and not request.user == project.author:

#             # Stores log-in prompt message to be displayed with redirect request
#             messages.add_message(request, messages.WARNING, 'Du har ikke tilgang til artikkelen')

#             return redirect("/")

#         return super(ProjectView, self).dispatch(request, *args, **kwargs)






# # lager nytt prosjekt i arkivet
# class ProjectCreateView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
#     model = Project
#     form_class = ProjectForm
#     template_name = 'project/edit_project.html'
#     permission_required = 'project.add_project'            # Se på dette senere for permission til arkivet

#     def get_success_message(self, cleaned_data):
#         if self.object.draft:
#             return "Prosjektet er opprettet som utkast"
#         return "Prosjektet er opprettet og publisert"

#     def get_success_url(self):
#         return reverse('project:details', kwargs={'pk': self.object.id})

#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         return super().form_valid(form)



# # ----------------------------------------------------------------------------------
# # Viser ting som liste
# class ProjectListView(ListView):
#     model = Project
#     template_name = "project/project_list.html"
#     paginate_by = 10

#     def get_queryset(self):
#         # Retrieve published articles (so no drafts)
#         projects = Project.objects.order_by('-pub_date').filter(draft=False)
#         return projects.filter(internal=False)

#     def get_context_data(self, **kwargs):

#         context = super().get_context_data(**kwargs)

#         context['indicator_text'] = self.get_internal_articles_indicator()

#         # Retrieve any user drafts if logged in
#         if self.request.user.has_perm("project.add_article"):
#             context['drafts'] = Project.objects.order_by('-pub_date').filter(author=self.request.user,draft=True)

#         return context
# # ----------------------------------------------------------------------------------


# class ProjectUpdateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
#     model = Project
#     form_class = ProjectForm
#     template_name = "project/edit_project.html"
#     permission_required = "project.change_article"
#     success_message = "Prosjektartikkelen er oppdatert."

#     def get_success_url(self):
#         return reverse('project:details', kwargs={'pk': self.object.id})



# class ProjectDeleteView(PermissionRequiredMixin, DeleteView):
#     model = Project
#     success_url = "/project/"
#     permission_required = "project.delete_article"




