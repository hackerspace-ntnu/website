from datetime import date, datetime, timedelta

from dateutil.relativedelta import relativedelta
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
)

from inventory.models.item import Item
from inventory.models.item_loan import ItemLoan
from userprofile.models import Profile


class ItemLoanListView(PermissionRequiredMixin, ListView):
    """View for viewing all loan applications"""

    model = ItemLoan
    permission_required = "inventory.view_itemloan"
    template_name = "inventory/loan_applications.html"
    context_object_name = "applications"

    def get_queryset(self):
        application_filter = self.request.GET.get("filter", "")
        name_filter = self.request.GET.get("filter_name", "")

        applications = ItemLoan.objects.all()
        if application_filter == "overdue":
            # very roundabout way but we need applications to be a queryset
            applications = ItemLoan.objects.filter(
                id__in=[app.id for app in applications if app.overdue()]
            )
        elif application_filter == "not_approved":
            applications = ItemLoan.objects.filter(approver__isnull=True)
        elif application_filter == "open":
            applications = ItemLoan.objects.filter(approver__isnull=False)

        # Additionally filter by the name of the applicant
        if name_filter:
            applications = applications.filter(contact_name__icontains=name_filter)

        return applications.order_by("loan_to")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = self.request.GET.get("filter", "")
        context["filter_name"] = self.request.GET.get("filter_name", "")
        return context


class ItemLoanDetailView(PermissionRequiredMixin, DetailView):
    """View for a single loan application"""

    model = ItemLoan
    permission_required = "inventory.view_itemloan"
    template_name = "inventory/loan_detail.html"
    context_object_name = "app"


class ItemLoanApproveView(PermissionRequiredMixin, TemplateView):
    """Endpoint for approving loans"""

    permission_required = "inventory.view_itemloan"
    success_message = "Lånet er godkjent"

    def get_success_url(self, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().get_success_url(self, *args, **kwargs)

    def get(self, request, pk=None, **kwargs):
        if not pk:
            return HttpResponseRedirect(reverse("inventory:loans"))

        application = get_object_or_404(ItemLoan, id=pk)

        # trust no-one. not even hackerspace members
        if (
            application.amount > application.item.available()
            and not application.item.unknown_stock
        ):
            return HttpResponseRedirect(reverse("inventory:loans"))

        application.loan_from = timezone.now()
        application.approver = request.user
        application.save()

        return HttpResponseRedirect(
            reverse("inventory:loan_application", kwargs={"pk": pk})
        )


class ItemLoanDeclineView(PermissionRequiredMixin, DeleteView):
    """Endpoint for deleting/rejecting loans"""

    model = ItemLoan
    permission_required = "inventory.delete_itemloan"
    success_message = "Lånesøknaden er avslått"
    success_url = reverse_lazy("inventory:loans")

    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return self.success_url

    # Bypass the confirmation (we use a modal)
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class ItemLoanReturnedView(PermissionRequiredMixin, DeleteView):
    """Endpoint for returning loans (deletes them)"""

    model = ItemLoan
    permission_required = "inventory.delete_itemloan"
    success_message = "Lånesøknaden er lukket"
    success_url = reverse_lazy("inventory:loans")

    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return self.success_url

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class ItemLoanApplicationView(CreateView):
    """View for applying for loans"""

    model = ItemLoan
    fields = [
        "item",
        "amount",
        "loan_from",
        "loan_to",
        "purpose",
        "contact_name",
        "contact_phone",
        "contact_email",
        "consent",
    ]
    template_name = "inventory/loan_apply.html"
    success_message = "Lånesøknaden er registrert!"
    success_url = reverse_lazy("inventory:inventory")
    months_max_ahead = 1

    def get_success_url(self):
        # SuccessMessageMixin doesn't actually work so fuck it
        messages.success(self.request, self.success_message)
        return self.success_url

    def get_initial(self, *args, **kwargs):
        user = self.request.user
        if user and user.is_authenticated:
            initial_form = {
                "contact_name": "{} {}".format(user.first_name, user.last_name),  # her
                "contact_email": user.email,
            }

            # Phone numbers are stored separately in the associated user profile
            profile = Profile.objects.get(user=user)
            if profile:
                initial_form["contact_phone"] = profile.phone_number

            return initial_form

        return None

    def get(self, *args, **kwargs):
        pk = kwargs.get("pk", -1)
        if pk == -1:
            return super().get(*args, **kwargs)

        item = get_object_or_404(Item, id=pk)
        # Go back to the inventory view if the item has no stock in inventory
        # Same if you're not allowed to loan the item
        if not item.in_stock() or not item.can_loan:
            return HttpResponseRedirect(self.success_url)

        return super().get(*args, **kwargs)

    def get_form(self, *args, **kwargs):
        # Add the datepicker class to the loan to field before it's sent off
        form = super().get_form(*args, **kwargs)
        form.fields["loan_to"].widget.attrs["class"] = "datepicker"
        form.fields["loan_from"].widget.attrs["class"] = "datepicker"
        form.fields["loan_from"].widget.format = "%d.%m.%Y"  # Set date format
        form.fields["loan_to"].widget.format = "%d.%m.%Y"  # Set date format
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["item"] = Item.objects.get(id=self.kwargs["pk"])
        context["loan_from_max_date"] = date.today() + relativedelta(
            months=self.months_max_ahead
        )
        return context

    def form_valid(self, form):
        item = self.get_context_data().get("item")
        if not item.can_loan:
            return HttpResponseRedirect(reverse("inventory:inventory"))

        # can always loan items whose stock is unknown
        if form.instance.amount > item.stock and not item.unknown_stock:
            form.errors["amount"] = "Du kan ikke be om å låne mer enn vi har på lager"
            return self.render_to_response(self.get_context_data(form=form))

        max_duration = Item.objects.get(id=self.kwargs["pk"]).max_loan_duration
        # Convert 'loan to' date from datetime.date to datetime.datetime (i.e. add time 00:00)
        # (because same type is required for the comparison check)
        loan_from_datetime = datetime.combine(
            form.instance.loan_from, datetime.max.time()
        )
        loan_to_datetime = datetime.combine(form.instance.loan_to, datetime.min.time())

        if max_duration and loan_to_datetime > loan_from_datetime + timedelta(
            days=max_duration
        ):
            form.errors[
                "loan_to"
            ] = f"Du kan ikke låne denne gjenstanden lenger enn {max_duration} dager"
            return self.render_to_response(self.get_context_data(form=form))
        if loan_to_datetime < loan_from_datetime:
            form.errors["loan_from"] = "Startdato for lån må være før sluttdato for lån"
            return self.render_to_response(self.get_context_data(form=form))
        if loan_from_datetime < datetime.now():
            form.errors[
                "loan_from"
            ] = "Du kan ikke starte å låne denne gjenstanden før i dag"
            return self.render_to_response(self.get_context_data(form=form))
        if loan_from_datetime.date() > (
            date.today() + relativedelta(months=self.months_max_ahead)
        ):
            form.errors[
                "loan_from"
            ] = f"""Du kan ikke starte å låne denne gjenstanden mer enn {self.months_max_ahead} måned frem i tid"""
            return self.render_to_response(self.get_context_data(form=form))

        # bit ugly but it works
        user = self.request.user
        if self.request.POST.get("autoapprove") and user.has_perm(
            "inventory.view_itemloan"
        ):
            application = form.instance
            application.loan_from = timezone.now()
            application.approver = user
            application.save()

        return super().form_valid(form)
