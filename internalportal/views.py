from datetime import datetime

from django.contrib import messages
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
)
from django.contrib.auth.views import HttpResponseRedirect
from django.shortcuts import redirect
from django.views.generic import (
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    View,
)
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.db.models import OuterRef, Q, Subquery
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _

from applications.models import Application, ApplicationGroup, ApplicationGroupChoice
from committees.models import Committee
from inventory.models.item_loan import ItemLoan
from news.models import Article, Event


class InternalPortalView(PermissionRequiredMixin, TemplateView):
    template_name = "internalportal/internalportal.html"
    permission_required = "userprofile.is_active_member"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context["current_date"] = datetime.now()

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


class ApplicationsView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = "internalportal/applications.html"
    permission_required = "userprofile.is_active_member"
    context_object_name = "applications"

    def test_func(self):
        return get_commitee_with_leader(self.request.user) is not None

    def handle_no_permission(self):
        # TODO: Display page asking user to log in if they are not
        return redirect("/")

    def get_queryset(self):
        committee = get_commitee_with_leader(self.request.user)
        application_group = ApplicationGroup.objects.filter(name=committee.name).first()

        print(application_group, committee)
        min_priority_subquery = (
            ApplicationGroupChoice.objects.filter(
                group=OuterRef("applicationgroupchoice__group__id")
            )
            .order_by("priority")
            .values("priority")[:1]
        )

        return Application.objects.filter(
            applicationgroupchoice__priority=Subquery(min_priority_subquery),
            applicationgroupchoice__group=application_group,
        )


class ApplicationView(DetailView):
    model = Application
    template_name = "internalportal/application.html"
    context_object_name = "application"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        groups = self.get_object().applicationgroupchoice_set.all().order_by("priority")
        print(groups)
        context["second_group"] = groups[1] if groups.count() > 1 else None
        return context


class ApplicationNextGroupView(View, UserPassesTestMixin):
    """Send an application to the next group"""

    success_url = reverse_lazy("internalportal:applications")
    success_message = _("Søknad sendt videre til neste gruppe")

    def test_func(self):
        return get_commitee_with_leader(self.request.user) is not None

    def get(self, request, *args, **kwargs):
        application = Application.objects.filter(id=kwargs.get("pk")).first()
        if not application:
            messages.error(request, _("Søknaden finnes ikke"))
            return HttpResponseRedirect(reverse_lazy("internalportal:applications"))
        new_application_message = render_to_string(
            "applications/new_application_email.txt",
            {"applications_url": reverse("internalportal:applications")},
        )
        next_application_groups = application.applicationgroupchoice_set.order_by(
            "priority"
        )
        if next_application_groups.count() < 2:
            messages.error(request, _("Søknaden har ingen flere grupper å gå til"))
            return HttpResponseRedirect(reverse_lazy("internalportal:applications"))
        next_group = next_application_groups[1]
        committee = Committee.objects.filter(name=next_group.group.name).first()
        emails = [
            getattr(committee.main_lead, "email", None),
            getattr(committee.second_lead, "email", None),
        ]
        if not any(emails):
            messages.error(request, _("Gruppen har ingen ledere"))
            return

        send_mail(
            _("Søknad sendt videre"),
            new_application_message,
            "Hackerspace NTNU",
            emails,
            fail_silently=False,
        )

        ApplicationGroupChoice.objects.filter(application=application).order_by(
            "priority"
        ).first().delete()
        return HttpResponseRedirect(reverse_lazy("internalportal:applications"))


class ApplicationProcessView(UserPassesTestMixin, DeleteView):
    model = Application
    template_name = "internalportal/applications/application_confirm_delete.html"
    success_url = "/internalportal/applications/"

    def test_func(self):
        commitee = get_commitee_with_leader(self.request.user)
        if commitee is None:
            return False
        application = self.get_object()
        return (
            application.group_choice.order_by("priority").first().name == commitee.name
        )


def get_commitee_with_leader(user):
    query = Q(main_lead=user.id) | Q(second_lead=user.id)
    return Committee.objects.filter(query).first()
