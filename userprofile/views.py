from django.contrib.auth.models import User
# For merging user and profile forms
from django.forms import inlineformset_factory, widgets
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.http import Http404

import re

from .forms import ProfileSearchForm
from .models import Profile, Skill
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
        profiles = Profile.objects.filter(user__groups__name='member', user__first_name__icontains=filter_val).all()
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
        try:
            userprofile = self.request.user.profile
            return userprofile
        except AttributeError:
            raise Http404("Profile not found")

class ProfileDetailView(DetailView):
    # Vis en spesifikk profil.
    # Endpointet her er /profile/<id>
    template_name = "userprofile/profile.html"

    def get_object(self):
        # Get the user for the pk, then return the user profile
        pk = self.kwargs['pk']
        user = get_object_or_404(User, pk=pk)
        return get_object_or_404(Profile, pk=user.profile.pk)

class ProfileUpdateView(UpdateView):
    # Klasse for å oppdatere brukerprofilen sin
    model = Profile
    fields = ['image', 'access_card', 'study', 'skills', 'social_discord', 'social_steam', 'social_battlenet', 'social_git']
    template_name = "userprofile/edit_profile.html"
    success_url = "/profile"

    def get_object(self):
        try:
            userprofile = self.request.user.profile
            return userprofile
        except AttributeError:
            raise Http404("Profile not found")
