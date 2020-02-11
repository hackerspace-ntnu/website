from django.contrib.auth.models import User
# For merging user and profile forms
from django.shortcuts import get_object_or_404
from django.http import Http404
from committees.models import Committee
from .forms import ProfileSearchForm
from .models import Profile, Skill, TermsOfService
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import CreateView
from django.shortcuts import redirect
from django.urls import reverse

class ProfileListView(ListView):
    # Lister opp alle brukerprofiler med pagination
    model = Profile
    form_class = ProfileSearchForm
    paginate_by = 9
    template_name = "userprofile/profile_list.html"

    # Søkefunksjonalitet som filtrerer queryset
    def get_queryset(self):
        filter_val = self.request.GET.get('filter', '')
        committee_array = Committee.objects.values_list('name', flat=True)
        profiles = Profile.objects.filter(user__groups__name__in=list(committee_array), user__first_name__icontains=filter_val).order_by('user__first_name')
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

class ProfileUpdateView(SuccessMessageMixin, UpdateView):
    # Klasse for å oppdatere brukerprofilen sin
    model = Profile
    fields = ['image', 'access_card', 'study', 'show_email', 'skills', 'social_discord', 'social_steam', 'social_battlenet', 'social_git', 'allergi_gluten', 'allergi_vegetar', 'allergi_vegan', 'allergi_annet', 'limit_social', 'phone_number']
    template_name = "userprofile/edit_profile.html"
    success_url = "/profile"
    success_message = "Profilen er oppdatert."

    def get_object(self):
        try:
            userprofile = self.request.user.profile
            return userprofile
        except AttributeError:
            raise Http404("Profile not found")


class TermsOfServiceView(DetailView):
    model = TermsOfService
    template_name = "userprofile/tos_detail.html"

class MostRecentTermsOfServiceView(TermsOfServiceView):

    def get_object(self):
        return TermsOfService.objects.order_by('-pub_date').first()


class TermsOfServiceCreateView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):

    model = TermsOfService
    fields = ['text', 'pub_date']
    template_name = "userprofile/edit_tos.html"
    permission_required = "userprofile.add_termsofservice"
    success_message = "TOS er opprettet"

    def get_success_url(self):
        return reverse('tos-details', kwargs={'pk': self.object.id})


class TermsOfServiceEditView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):

    model = TermsOfService
    template_name = "userprofile/edit_tos.html"
    fields = ['text', 'pub_date']
    permission_required = "userprofile.change_termsofservice"
    success_message = "TOS er oppdatert"

    def get_success_url(self):
        return reverse('tos-details', kwargs={'pk': self.object.id})

class MostRecentTermsOfServiceEditView(TermsOfServiceEditView):

    def get_object(self):
        return TermsOfService.objects.order_by('-pub_date').first()
