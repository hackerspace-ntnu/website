# from typing import Any

from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.paginator import Paginator

# from django.http import HttpRequest
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    FormView,
    TemplateView,
    UpdateView,
)
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from inventory.forms import ItemsUploadForm
from inventory.models.item import Item
from inventory.upload_script import upload


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


class ItemUploadView(PermissionRequiredMixin, FormView):
    template_name = "inventory/upload_item.html"
    permission_required = "inventory.change_item"
    success_url = reverse_lazy("inventory:inventory")
    form_class = ItemsUploadForm

    def form_valid(self, form):
        formvalid = super().form_valid(form)
        if formvalid:
            data = form.cleaned_data["file"].read().decode("utf-8")
            print("\n\n" + data + "\n\n")
            upload(data)
            return formvalid


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
