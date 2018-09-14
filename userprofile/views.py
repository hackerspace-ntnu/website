from django.contrib.auth.models import User
# For merging user and profile forms
from django.forms import inlineformset_factory, widgets
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required

import re

from .forms import UserForm, ProfileForm, ProfileFormSet, ProfileSearchForm
from .models import Profile, Skill, Group
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.forms import modelformset_factory, formset_factory

class ProfileListView(ListView):
    # Lister opp alle brukerprofiler med pagination
    model = Profile
    form_class = ProfileSearchForm
    paginate_by = 3
    template_name = "userprofile/profile_list.html"

    # Søkefunksjonalitet som filtrerer queryset
    def get_queryset(self):
        filter_val = self.request.GET.get('filter', '')
        profiles = Profile.objects.filter(user__first_name__icontains=filter_val).all()
        return profiles

    def get_context_data(self, **kwargs):
        context = super(ProfileListView, self).get_context_data(**kwargs)
        context['filter'] = self.request.GET.get('filter', '')
        return context

class SelfProfileDetailView(DetailView):
    # Vis egen profil.
    # Endpointet her er /profile/
    template_name = "userprofile/profile.html"
    model = Profile

    def get_object(self):
        return get_object_or_404(Profile, pk=self.request.user.profile.id)

class ProfileDetailView(DetailView):
    # Vis en spesifikk profil.
    # Endpointet her er /profile/<id>
    template_name = "userprofile/profile.html"
    model = Profile

class ProfileUpdateView(UpdateView):
    # Klasse for å oppdatere brukerprofilen sin

    # Modellen tar utgangspunkt i djangos brukerobject User, men legger
    # til en profile-form fra ProfileFormSet som senere settes inn i User objektet.
    # Formålet med dette er å kunne redigere både User og Profile samtidig.
    model = User
    form_class = UserForm
    template_name = "userprofile/edit_profile.html"
    success_url = "/profile"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset = ProfileFormSet(
            request.POST,
            request.FILES,
            instance=self.object)

        if form.is_valid():
            if formset.is_valid():
                formset.save()
                return self.form_valid(form)
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(ProfileUpdateView, self).get_context_data(**kwargs)
        form = UserForm(instance=self.object)

        context['formset'] =  ProfileFormSet(instance=self.object)
        return context

    def get_object(self):
        return get_object_or_404(User, pk=self.request.user.id)


#TODO: Class based skill views
