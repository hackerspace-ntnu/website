from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from news.models import Article, Event
from door.models import DoorStatus
from userprofile.models import TermsOfService
from committees.models import Committee
from userprofile.models import Profile
from datetime import datetime
from applications.models import ApplicationPeriod
from .models import Card, FaqQuestion, Rule
from django.views.generic import ListView, TemplateView, RedirectView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from urllib import parse as urlparse


class AcceptTosView(TemplateView):
    template_name = 'website/tos-returningls.html'

    def get(self, request, *args, **kwargs):

        if not self.request.user.is_authenticated or self.request.user.profile.has_accepted_most_recent_tos():
            # No user logged in, or user has already accepted TOS, return to main page
            return redirect("/")

        # Get originally visited page before TOS "pop-up"
        refererUrl = request.META.get('HTTP_REFERER')

        # Make sure page is valid before storing it for later
        if refererUrl:
            # Save users pre-TOS page path in session variable
            # Parse converts from absolute to relative path
            request.session['redirect_after_tos_accept'] = urlparse.urlparse(refererUrl).path

        return super().get(self, request, *args, **kwargs)


class AcceptTosRedirectView(LoginRequiredMixin, RedirectView):
    pattern_name = 'index'

    def get_redirect_url(self, *args, **kwargs):
        profileobj = get_object_or_404(Profile, pk=self.request.user.profile.id)
        if (profileobj != None):
            mostRecentTos = TermsOfService.objects.order_by('-pub_date').first();

            profileobj.accepted_tos = mostRecentTos
            profileobj.save()

        # Pop and redirect to pre-TOS path stored in session variable
        # Redirects to '/' if pop fails
        return self.request.session.pop('redirect_after_tos_accept', super().get_redirect_url(*args, **kwargs))


class AboutView(TemplateView):
    template_name = "website/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['committees'] = Committee.objects.filter(active=True).order_by("-priority")
        context['faq'] = FaqQuestion.objects.all()
        return context


class RulesView(TemplateView):
    template_name = "website/rules.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.has_perm('website.can_view_internal_rule'):
            context['rules'] = Rule.objects.order_by("-priority").filter(internal=False)
        else:
            context['rules'] = Rule.objects.order_by("-priority")
        return context


class RuleDetailsView(DetailView):

    model = Rule
    template_name = "website/rule_details.html"

    def dispatch(self, request, *args, **kwargs):
        rule = self.get_object()
        if rule.internal and not request.user.has_perm('website.can_view_internal_rule'):
            return redirect("/")
        return super(RuleDetailsView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rule'] = Rule.objects.get(id=self.object.pk)
        return context


class AdminView(PermissionRequiredMixin, TemplateView):
    template_name = "website/admin.html"
    permission_required = "userprofile.can_view_admin"

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

    def get_internal_articles_indicator(self):

        # Determine number of hidden internal articles
        if not self.request.user.has_perm('news.can_view_internal_article'):
            internal_articles_count = len(Article.objects.filter(internal=True, draft=False))
        else:
            internal_articles_count = 0

        badge_text = {
            "plural": {
                "large": "interne artikler skjult",
                "medium": "interne skjult",
                "small": "skjult"
            },
            "singular": {
                "large": "intern artikkel skjult",
                "medium": "intern skjult",
                "small": "skjult"
            }
        }

        return {
            'count': internal_articles_count,
            'badge_text': badge_text,
            'tooltip_text': "Trykk for å logge på og se interne artikler"
        }

    def get_internal_events_indicator(self):

        current_date = datetime.now()

        # Determine number of hidden internal events
        if not self.request.user.has_perm('news.can_view_internal_event'):
            upcoming_internal_events_count = len(
                Event.objects.filter(internal=True, draft=False).filter(time_start__gte=current_date))
        else:
            upcoming_internal_events_count = 0

        badge_text = {
            "plural": {
                "large": "interne arrangementer skjult",
                "medium": "interne skjult",
                "small": "skjult"
            },
            "singular": {
                "large": "internt arrangement skjult",
                "medium": "internt skjult",
                "small": "skjult"
            }
        }

        return {
            'count': upcoming_internal_events_count,
            'badge_text': badge_text,
            'tooltip_text': "Trykk for å logge på og se interne arrangementer"
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Sjekk om bruker har medlemskap og kan se interne elementer
        can_access_internal_article = self.request.user.has_perm('news.can_view_internal_article')
        can_access_internal_event = self.request.user.has_perm('news.can_view_internal_event')

        # First sort, then grab 5 elements, then flip the list ordered by date
        event_list = Event.objects.filter(
            internal__lte=can_access_internal_event, draft=False).order_by('-time_start')[:5:-1]

        current_date = datetime.now()

        # Get five published articles
        article_list = Article.objects.filter(
            internal__lte=can_access_internal_article, draft=False
        ).order_by('-pub_date')[:5]

        # Få dørstatus
        try:
            door_status = DoorStatus.objects.get(name='hackerspace').status
        except DoorStatus.DoesNotExist:
            door_status = True

        # hvis det ikke eksisterer en ApplicationPeriod, lag en.
        if not ApplicationPeriod.objects.filter(name="Opptak"):
            ap = ApplicationPeriod.objects.create(
                name="Opptak",
                period_start=datetime(2018, 1, 1),
                period_end=datetime(2018, 1, 2)
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
            'internal_articles_indicator': self.get_internal_articles_indicator(),
            'internal_events_indicator': self.get_internal_events_indicator(),
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
