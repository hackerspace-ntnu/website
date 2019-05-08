from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from news.models import Article, Event
from door.models import DoorStatus
from committees.models import Committee
from userprofile.models import Profile
from datetime import datetime
from applications.models import ApplicationPeriod
from .models import Card, FaqQuestion
from django.views.generic import ListView, TemplateView, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

class AcceptTosRedirectView(LoginRequiredMixin, RedirectView):
    pattern_name = 'index'

    def get_redirect_url(self, *args, **kwargs):
        profileobj = get_object_or_404(Profile, pk=self.request.user.profile.id)
        if(profileobj != None):
            profileobj.tos_accepted = True
            profileobj.save()

        return super().get_redirect_url(*args, **kwargs)

class AboutView(TemplateView):
    template_name = "website/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['committees'] = Committee.objects.all()
        context['faq'] = FaqQuestion.objects.all()
        return context


class AdminView(PermissionRequiredMixin, TemplateView):
    template_name = "website/admin.html"
    permission_required = "can_view_admin"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get all users belonging to a committee as well as pang
        committee_array = list(Committee.objects.values_list('name', flat=True))
        committee_array.append('Pang')
        profiles = Profile.objects.filter(user__groups__name__in=committee_array).order_by('user__first_name')

        context['profiles'] = profiles
        return context

class IndexView(TemplateView):
    template_name = "website/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Sjekk om bruker har medlemskap og kan se interne elementer
        can_access_internal_article = self.request.user.has_perm('news.can_view_internal_article')
        can_access_internal_event = self.request.user.has_perm('news.can_view_internal_event')

        # First sort, then grab 5 elements, then flip the list ordered by date
        event_list = Event.objects.filter(
            internal__lte=can_access_internal_event).order_by('-time_start')[:5:-1]

        # Get five articles
        article_list = Article.objects.filter(
            internal__lte=can_access_internal_article).order_by('-pub_date')[:5]

        # Få dørstatus
        try:
            door_status = DoorStatus.objects.get(name='hackerspace').status
        except DoorStatus.DoesNotExist:
            door_status = True

        current_date = datetime.now()

        # hvis det ikke eksisterer en ApplicationPeriod, lag en.
        if not ApplicationPeriod.objects.filter(name="Opptak"):
            ap = ApplicationPeriod.objects.create(
                name="Opptak",
                period_start=datetime(2018,1,1),
                period_end=datetime(2018,1,2)
                ).save()

        app_start_date = ApplicationPeriod.objects.get(name="Opptak").period_start
        app_end_date = ApplicationPeriod.objects.get(name="Opptak").period_end
        if (current_date < app_start_date) or (current_date > app_end_date):
            is_application = False
        else:
            is_application = True

        context = {
            'article_list': article_list,
            'event_list': event_list,
            'door_status': door_status,
            'app_start_date': app_start_date,
            'app_end_date': app_end_date,
            'is_application': is_application,
            'index_cards': Card.objects.all(),
            'current_date': current_date
        }

        return context


def handler404(request, exception=None):
    return render(request, 'website/404.html', status=404)


def handler500(request, exception=None):
    return render(request, 'website/500.html', status=500)
