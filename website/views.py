from datetime import datetime
from random import randint
from urllib import parse as urlparse

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.generic import DetailView, RedirectView, TemplateView

from applications.models import ApplicationPeriod
from committees.models import Committee
from door.models import DoorStatus
from inventory.models import ItemLoan
from news.models import Article, Event
from userprofile.models import Profile, TermsOfService

from .models import Card, FaqQuestion, Rule
from .settings import INTRANET_GREETINGS


class AcceptTosView(TemplateView):
    template_name = "website/tos-returningls.html"

    def get(self, request, *args, **kwargs):

        if (
            not self.request.user.is_authenticated
            or self.request.user.profile.has_accepted_most_recent_tos()
        ):
            # No user logged in, or user has already accepted TOS, return to main page
            return redirect("/")

        # Get originally visited page before TOS "pop-up"
        refererUrl = request.META.get("HTTP_REFERER")

        # Make sure page is valid before storing it for later
        if refererUrl:
            # Save users pre-TOS page path in session variable
            # Parse converts from absolute to relative path
            request.session["redirect_after_tos_accept"] = urlparse.urlparse(
                refererUrl
            ).path

        return super().get(self, request, *args, **kwargs)


class AcceptTosRedirectView(LoginRequiredMixin, RedirectView):
    pattern_name = "index"

    def get_redirect_url(self, *args, **kwargs):
        profile = get_object_or_404(Profile, pk=self.request.user.profile.id)
        if profile is not None:
            most_recent_tos = TermsOfService.objects.order_by("-pub_date").first()

            profile.accepted_tos = most_recent_tos
            profile.save()

        # Pop and redirect to pre-TOS path stored in session variable
        # Redirects to '/' if pop fails
        return self.request.session.pop(
            "redirect_after_tos_accept", super().get_redirect_url(*args, **kwargs)
        )


class AboutView(TemplateView):
    template_name = "website/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["committees"] = Committee.objects.filter(active=True).order_by(
            "-priority"
        )
        context["faq"] = FaqQuestion.objects.all()
        return context


class RulesView(TemplateView):
    template_name = "website/rules.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.has_perm("website.can_view_internal_rule"):
            context["rules"] = Rule.objects.order_by("-priority").filter(internal=False)
        else:
            context["rules"] = Rule.objects.order_by("-priority")
        return context


class RuleDetailsView(DetailView):

    model = Rule
    template_name = "website/rule_details.html"

    def dispatch(self, request, *args, **kwargs):
        rule = self.get_object()
        if rule.internal and not request.user.has_perm(
            "website.can_view_internal_rule"
        ):
            return redirect("/")
        return super(RuleDetailsView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["rule"] = Rule.objects.get(id=self.object.pk)
        return context


class AdminView(PermissionRequiredMixin, TemplateView):
    template_name = "website/admin.html"
    permission_required = "userprofile.can_view_admin"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get all users belonging to a committee as well as pang
        committee_array = list(Committee.objects.values_list("name", flat=True))
        committee_array.append("Pang")
        profiles = Profile.objects.filter(
            user__groups__name__in=committee_array
        ).order_by("user__first_name")

        context["profiles"] = profiles
        return context


class IndexView(TemplateView):
    template_name = "website/index.html"

    def get_internal_articles_indicator(self):

        # Determine number of hidden internal articles
        if not self.request.user.has_perm("news.can_view_internal_article"):
            internal_articles_count = len(
                Article.objects.filter(internal=True, draft=False)
            )
        else:
            internal_articles_count = 0

        badge_text = {
            "plural": {
                "large": "interne artikler skjult",
                "medium": "interne skjult",
                "small": "skjult",
            },
            "singular": {
                "large": "intern artikkel skjult",
                "medium": "intern skjult",
                "small": "skjult",
            },
        }

        return {
            "count": internal_articles_count,
            "badge_text": badge_text,
            "tooltip_text": "Trykk for å logge på og se interne artikler",
        }

    def get_internal_events_indicator(self):

        current_date = datetime.now()

        # Determine number of hidden internal events
        if not self.request.user.has_perm("news.can_view_internal_event"):
            upcoming_internal_events_count = len(
                Event.objects.filter(internal=True, draft=False).filter(
                    time_start__gte=current_date
                )
            )
        else:
            upcoming_internal_events_count = 0

        badge_text = {
            "plural": {
                "large": "interne arrangementer skjult",
                "medium": "interne skjult",
                "small": "skjult",
            },
            "singular": {
                "large": "internt arrangement skjult",
                "medium": "internt skjult",
                "small": "skjult",
            },
        }

        return {
            "count": upcoming_internal_events_count,
            "badge_text": badge_text,
            "tooltip_text": "Trykk for å logge på og se interne arrangementer",
        }

    def get_context_data(self, **kwargs):

        # Sjekk om bruker har medlemskap og kan se interne elementer
        can_access_internal_article = self.request.user.has_perm(
            "news.can_view_internal_article"
        )
        can_access_internal_event = self.request.user.has_perm(
            "news.can_view_internal_event"
        )

        # Get the 5 events closest to starting
        event_list = list(
            Event.objects.filter(
                time_start__gt=timezone.now(),
                internal__lte=can_access_internal_event,
                draft=False,
            ).order_by("time_start")[:5]
        )

        # Add expired events if we couldn't fill the 5 slots
        if len(event_list) < 5:
            to_fill = 5 - len(event_list)
            expired_events = Event.objects.filter(
                time_start__lte=timezone.now(),
                internal__lte=can_access_internal_event,
                draft=False,
            ).order_by("-time_start")[:to_fill]
            event_list += list(expired_events)

        current_date = datetime.now()

        # Get five published articles
        article_list = Article.objects.filter(
            internal__lte=can_access_internal_article, draft=False
        ).order_by("-pub_date")[:5]

        # Få dørstatus
        try:
            door_status = DoorStatus.objects.get(name="hackerspace").status
        except DoorStatus.DoesNotExist:
            door_status = True

        app_period = ApplicationPeriod.objects.filter(name="Opptak").first()

        return {
            **super().get_context_data(**kwargs),
            "article_list": article_list,
            "event_list": event_list,
            "internal_articles_indicator": self.get_internal_articles_indicator(),
            "internal_events_indicator": self.get_internal_events_indicator(),
            "door_status": door_status,
            "app_end_date": app_period.period_end if app_period else None,
            "is_application": app_period and app_period.is_open(),
            "index_cards": Card.objects.all(),
            "current_date": current_date,
        }


class IntranetView(PermissionRequiredMixin, TemplateView):
    template_name = "website/intranet.html"
    permission_required = "userprofile.is_active_member"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context["current_date"] = datetime.now()

        # Random greeting for the intranet header banner. Just for fun
        greeting = INTRANET_GREETINGS[randint(0, len(INTRANET_GREETINGS) - 1)]
        # cba doing a regex or some other fancy stuff to check if the string has formatting
        # just break it till it works
        try:
            context["greeting"] = greeting.format(self.request.user.first_name)
        except IndexError:
            context["greeting"] = greeting

        # Find the 5 loan apps that have gone unapproved the longest
        context["loan_app_list"] = ItemLoan.objects.filter(
            approver__isnull=True,
        ).order_by("-loan_from")[:5]

        # Same as in the index view
        context["event_list"] = Event.objects.filter(internal=True).order_by(
            "-time_start"
        )[:5]

        context["article_list"] = Article.objects.filter(
            internal=True, draft=False
        ).order_by("-pub_date")[:5]

        return context


def handler404(request, exception=None):
    return render(request, "website/404.html", status=404)


def handler403(request, exception=None):
    return render(request, "website/403.html", status=403)


def handler500(request, exception=None):
    return render(request, "website/500.html", status=500)
