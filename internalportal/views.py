from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib import messages
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
)
from django.contrib.auth.models import Group
from django.contrib.auth.views import HttpResponseRedirect
from django.core.mail import send_mail
from django.db.models import OuterRef, Q, Subquery
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import DeleteView, DetailView, ListView, TemplateView
from django.views.generic.edit import BaseDetailView

from applications.models import Application, ApplicationGroup, ApplicationGroupChoice
from authentication.views import get_user_by_stud_or_ntnu_email
from committees.models import Committee
from inventory.models.item_loan import ItemLoan
from news.models import Article, Event


class InternalPortalView(PermissionRequiredMixin, TemplateView):
    template_name = "internalportal/internalportal.html"
    permission_required = "userprofile.is_active_member"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context["current_date"] = datetime.now()
        context["next_year"] = datetime.now() + timedelta(days=365)

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

        context["door_access_member_list"] = (
            get_user_model()
            .objects.filter(groups__name="Medlem")
            .order_by("-date_joined")
        )

        return context


class ApplicationsView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = "internalportal/applications/applications.html"
    permission_required = "userprofile.is_active_member"
    context_object_name = "applications"

    def test_func(self):
        return get_commitee_with_leader(self.request.user) is not None

    def handle_no_permission(self):
        # TODO: Display page asking user to log in if they are not
        return redirect("/")

    def get_queryset(self):
        committee = get_commitee_with_leader(self.request.user)
        if not committee:
            return Application.objects.none()
        application_group = ApplicationGroup.objects.filter(name=committee.name).first()

        first_group = (
            ApplicationGroupChoice.objects.filter(application=OuterRef("id"))
            .order_by("priority")
            .values("group")[:1]
        )

        return (
            Application.objects.filter(applicationgroupchoice__group=application_group)
            .annotate(first_group=Subquery(first_group))
            .filter(first_group=application_group)
        )


class ApplicationView(UserPassesTestMixin, DetailView):
    model = Application
    template_name = "internalportal/applications/application.html"
    context_object_name = "application"

    def test_func(self):
        committee = get_commitee_with_leader(self.request.user)
        return first_application_group_is_committee(self.get_object(), committee)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        groups = self.get_object().applicationgroupchoice_set.all().order_by("priority")
        context["second_group"] = groups[1] if groups.count() > 1 else None
        return context


class ApplicationNextGroupView(UserPassesTestMixin, BaseDetailView):
    """Send an application to the next group"""

    model = Application
    success_url = reverse_lazy("internalportal:applications")
    success_message = _("Søknad sendt videre til neste gruppe")

    def test_func(self):
        committee = get_commitee_with_leader(self.request.user)
        return first_application_group_is_committee(self.get_object(), committee)

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

        if not committee:
            messages.error(
                request,
                _("Gruppen {group_name} finnes ikke. Kontakt administrator.").format(
                    group_name=next_group.group.name
                ),
            )
            return HttpResponseRedirect(reverse_lazy("internalportal:applications"))

        emails = [
            getattr(committee.main_lead, "email", None),
            getattr(committee.second_lead, "email", None),
        ]
        if not any(emails):
            messages.error(
                request,
                _("Gruppen {group} har ingen ledere").format(group=committee.name),
            )
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


class ApplicationRemoveView(UserPassesTestMixin, DeleteView):
    model = Application
    template_name = "internalportal/applications/application_confirm_delete.html"
    success_url = "/internalportal/applications/"

    def test_func(self):
        committee = get_commitee_with_leader(self.request.user)
        return first_application_group_is_committee(self.get_object(), committee)


class ApplicationApproveView(ApplicationRemoveView):
    template_name = "internalportal/applications/approve.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["group"] = (
            self.get_object()
            .applicationgroupchoice_set.order_by("priority")
            .first()
            .group
        )
        return context

    def delete(self, request, *args, **kwargs):

        # get email from request
        application = self.get_object()

        email = request.POST.get("email")
        if not email:
            email = application.email

        group_name = (
            application.applicationgroupchoice_set.order_by("priority")
            .first()
            .group.name
        )
        group = get_object_or_404(Group, name=group_name)

        # Force users to use their stud email in their application
        user = get_user_by_stud_or_ntnu_email(email)
        if not user:
            messages.error(
                request,
                _(
                    "Få brukeren til å logge inn med Feide først "
                    "og bruk søkerens ntnu-mail."
                ),
            )
            return HttpResponseRedirect(
                reverse_lazy(
                    "internalportal:application", kwargs={"pk": application.id}
                )
            )

        user.groups.add(group)
        user.groups.add(get_object_or_404(Group, name="Medlem"))
        user.save()

        # Send mail til søker

        return super().delete(request, *args, **kwargs)


def get_commitee_with_leader(user):
    query = Q(main_lead=user.id) | Q(second_lead=user.id)
    return Committee.objects.filter(query).first()


def first_application_group_is_committee(application, committee):
    if application is None or committee is None:
        return False
    return (
        application.applicationgroupchoice_set.order_by("priority").first().group.name
        == committee.name
    )
