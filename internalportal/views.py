from datetime import datetime

from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
)
from django.db.models import Q
from django.views.generic import TemplateView

from applications.models import Application, ApplicationGroup
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


class ApplicationsView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "internalportal/applications.html"
    permission_required = "userprofile.is_active_member"

    def test_func(self):
        return get_commitee_with_leader(self.request.user) is not None

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        commitee = get_commitee_with_leader(self.request.user)

        # FIXME: Why is a commitee not directly related to an application group?
        application_group = ApplicationGroup.objects.filter(name=commitee.name).first()

        application_query = Q(applicationgroupchoice__priority=1) & Q(
            applicationgroupchoice__group=application_group.id
        )
        context["applications"] = Application.objects.filter(application_query)
        return context


def get_commitee_with_leader(user):
    query = Q(main_lead=user.id) | Q(second_lead=user.id)
    return Committee.objects.filter(query).first()
