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
from django.db.models import Q
from django.shortcuts import redirect
from django.views.generic import (
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    View,
)
from django.urls import reverse_lazy
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
    template_name = "internalportal/applications.html"
    permission_required = "userprofile.is_active_member"
    context_object_name = "applications"

    def test_func(self):
        return get_commitee_with_leader(self.request.user) is not None

    def handle_no_permission(self):
        # TODO: Display page asking user to log in if they are not
        return redirect("/")

    def get_queryset(self):
        commitee = get_commitee_with_leader(self.request.user)

        # FIXME: Why is a commitee not directly related to an application group?
        application_group = ApplicationGroup.objects.filter(name=commitee.name).first()

        application_query = Q(applicationgroupchoice__priority=1) & Q(
            applicationgroupchoice__group=application_group.id
        )
        return Application.objects.filter(application_query)


class ApplicationView(DetailView):
    model = Application
    template_name = "internalportal/application.html"
    context_object_name = "application"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["next-group"] = (
            self.get_object().group_choice.order_by("priority").first()
        )
        return context


class ApplicationNextGroupView(View, UserPassesTestMixin):
    template_name = "internalportal/applications/next_group.html"
    success_url = "/internalportal/applications/"
    success_message = _("Søknad sendt videre til neste gruppe")

    def test_func(self):
        return get_commitee_with_leader(self.request.user) is not None

    def get(self, request, *args, **kwargs):
        application = Application.objects.filter(id=kwargs.get("pk")).first()
        if not application:
            messages.error(request, _("Søknaden finnes ikke"))
            return HttpResponseRedirect(reverse_lazy("internalportal:applications"))
        # send mail

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


# TODO: Connect application group with group directly
def get_group_of_application(application):
    application_group = application.group_choice.order_by("priority").first()
    return Group.objects.filter(name=getattr(application_group, "name")).first()


def get_commitee_with_leader(user):
    query = Q(main_lead=user.id) | Q(second_lead=user.id)
    return Committee.objects.filter(query).first()
