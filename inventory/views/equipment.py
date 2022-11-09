from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView

from inventory.models.equipment import Equipment


class EquipmentListView(ListView):
    """View for viewing all equipments"""

    model = Equipment
    permission_required = "inventory.view_equipment"
    template_name = "inventory/equipment/all_equipment.html"

    def get_queryset(self):
        return Equipment.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["items"] = self.get_queryset()
        return context


class EquipmentDeleteView(PermissionRequiredMixin, DeleteView):
    """Endpoint for deleting/rejecting loans"""

    model = Equipment
    permission_required = "inventory.delete_equipment"
    success_message = "Utstyret er slettet"
    success_url = reverse_lazy("inventory:equipment")

    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return self.success_url

    # Bypass the confirmation (we use a modal)
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class EquipmentCreateView(PermissionRequiredMixin, CreateView):
    """Endpoint for creating and updating equipment"""

    model = Equipment
    permission_required = "inventory.create_equipment"
    success_message = "Utstyr er registrert"
    template_name = "inventory/equipment/create_equipment.html"

    fields = [
        "name",
        "description",
        "thumbnail",
        "inventory_link",
    ]

    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return reverse("inventory:equipment", kwargs={"pk": self.object.id})
