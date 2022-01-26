from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.paginator import Paginator
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
    UpdateView,
)
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from userprofile.models import Profile

from .models import Item, ItemLoan


class InventoryListView(TemplateView):
    """
    Main view for the inventory page, containing a search module and utilizing
    the InventoryListAPIView to display a list of search result items
    """

    template_name = "inventory/inventory.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search"] = self.request.GET.get("search", "")
        context["page"] = self.request.GET.get("page", 1)
        context["sort_by"] = self.request.GET.get("sort_by", "")
        return context


class InventoryListAPIView(APIView):
    """
    API view returning an HTML response containing paginated items
    based on search, sorting and page number
    """

    renderer_classes = [TemplateHTMLRenderer]
    template_name = "inventory/items_list.html"
    paginate_by = 15

    def get(self, request):

        # Filter items based on search term
        search = self.request.GET.get("search", "")
        items = Item.objects.filter(name__icontains=search)

        # Sort according to url parameter
        sort_by = self.request.GET.get("sort_by", "")
        if sort_by == "name":
            items = items.order_by("name")
        elif sort_by == "stock_dsc":
            items = items.order_by("-stock")
        elif sort_by == "stock_asc":
            items = items.order_by("stock")
        elif sort_by == "popularity":
            items = sorted(items, key=lambda item: -item.popularity())
        else:
            # Default to sorting by ID (i.e. newest first)
            items = items.order_by("-id")

        # Paginate items
        paginator = Paginator(items, self.paginate_by)
        page_number = self.request.GET.get("page", 1)
        page_obj = paginator.page(page_number)

        return Response(
            {"items": page_obj.object_list, "sort_by": sort_by, "page_obj": page_obj}
        )


class ItemDetailView(DetailView):
    """Detail view for individual inventory items"""

    model = Item
    template_name = "inventory/item_detail.html"

    def get_object(self, *args, **kwargs):
        """Returns the result of the supercall, but tracks a view on the object"""
        obj = super().get_object(*args, **kwargs)
        if obj is None:
            return obj

        obj.views += 1
        obj.save()
        return obj


class ItemCreateView(PermissionRequiredMixin, CreateView):
    """View for creating new inventory items"""

    model = Item
    fields = [
        "name",
        "stock",
        "unknown_stock",
        "can_loan",
        "location",
        "max_loan_duration",
        "description",
        "thumbnail",
    ]
    template_name = "inventory/edit_item.html"
    permission_required = "inventory.add_item"
    success_message = "Gjenstanden er ført inn i lagersystemet."

    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return reverse("inventory:item", kwargs={"pk": self.object.id})

    def form_valid(self, form):
        if form.instance.stock < 0:
            form.errors["stock"] = "Lagerbeholdningen kan ikke være negativ"
            return self.render_to_response(self.get_context_data(form=form))
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class ItemUpdateView(PermissionRequiredMixin, UpdateView):
    """View for updating inventory items"""

    model = Item
    fields = [
        "name",
        "stock",
        "unknown_stock",
        "can_loan",
        "location",
        "max_loan_duration",
        "description",
        "thumbnail",
    ]
    template_name = "inventory/edit_item.html"
    permission_required = "inventory.change_item"
    success_message = "Lagerinnslaget er oppdatert."

    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return reverse("inventory:item", kwargs={"pk": self.object.id})

    def form_valid(self, form):
        if form.instance.stock < 0:
            form.errors["stock"] = "Lagerbeholdningen kan ikke være negativ"
            return self.render_to_response(self.get_context_data(form=form))
        return super().form_valid(form)


class ItemDeleteView(PermissionRequiredMixin, DeleteView):
    """View for deleting inventory items"""

    model = Item
    permission_required = "inventory.delete_item"
    success_url = reverse_lazy("inventory:inventory")
    success_message = "Lagerinnslaget er fjernet."

    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return self.success_url

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


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
            applications = applications.filter(contact_name__contains=name_filter)

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

    def get_success_url(self):
        # SuccessMessageMixin doesn't actually work so fuck it
        messages.success(self.request, self.success_message)
        return self.success_url

    def get_initial(self, *args, **kwargs):
        user = self.request.user
        if user and user.is_authenticated:
            initial_form = {
                "contact_name": "{} {}".format(user.first_name, user.last_name),
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
        max_duration = Item.objects.get(id=self.kwargs["pk"]).max_loan_duration
        if max_duration is not None:
            max_date = datetime.now() + timedelta(days=max_duration)
            form.fields["loan_to"].widget.attrs["data-max-date"] = max_date
        form.fields["loan_to"].widget.attrs["class"] = "datepicker"
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["item"] = Item.objects.get(id=self.kwargs["pk"])
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
        loan_to_datetime = datetime.combine(form.instance.loan_to, datetime.min.time())
        if loan_to_datetime > datetime.now() + timedelta(days=max_duration):
            form.errors[
                "loan_to"
            ] = f"Du kan ikke låne denne gjenstanden lenger enn {max_duration} dager"
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
