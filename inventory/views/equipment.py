from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from rest_framework import status, viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from inventory.models.equipment import Equipment
from inventory.serializers.equipment import EquipmentListSerializer


class EquipmentViewSet(viewsets.ModelViewSet):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentListSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return EquipmentListSerializer
        return EquipmentListSerializer


class EquipmentListView(ListView):
    """View for viewing all equipments"""

    model = Equipment
    permission_required = "inventory.view_equipment"
    template_name = "inventory/equipment/equipment_list.html"

    def get_queryset(self):
        return Equipment.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["items"] = self.get_queryset()
        return context


class EquipmentView(DetailView):
    model = Equipment
    template_name = "inventory/equipment/equipment.html"


class EquipmentCreateView(PermissionRequiredMixin, CreateView):
    """Endpoint for creating equipment"""

    model = Equipment
    permission_required = "inventory.create_equipment"
    success_message = "Utstyr er registrert"
    template_name = "inventory/equipment/equipment_edit.html"

    fields = [
        "name",
        "description",
        "thumbnail",
        "inventory_link",
    ]

    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return reverse("inventory:equipment_detail", kwargs={"pk": self.object.id})


class EquipmentEditView(EquipmentCreateView, UpdateView):
    """Endpoint for updating equipment. UpdateView overrides
    the create methods from CreateView"""

    permission_required = "inventory.edit_equipment"
    success_message = "Utstyret er oppdatert"


class EquipmentDeleteView(PermissionRequiredMixin, DeleteView):
    """Endpoint for deleting/rejecting loans"""

    model = Equipment
    permission_required = "inventory.delete_equipment"
    success_message = "Utstyret er slettet"
    success_url = reverse_lazy("inventory:equipment")
    template_name = "inventory/equipment/equipment_confirm_delete.html"

    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return self.success_url


class EquipmentChangeOrderApiView(APIView):
    """Endpoint for changing the order of equipment"""

    permission_classes = [IsAdminUser]

    def patch(self, request, pk, format=None):
        """Change the order of equipment"""
        try:
            equipment = Equipment.objects.get(pk=pk)
        except Equipment.DoesNotExist:
            return Response(
                {"status": "Equipment not found"}, status=status.HTTP_404_NOT_FOUND
            )
        self.change_order(equipment)
        equipment.save()
        return Response(
            {"status": "Equipment order changed"}, status=status.HTTP_200_OK
        )

    def change_order(self, equipment):
        """Override this method to choose how the order is changed"""
        pass


class EquipmentOrderUpApiView(EquipmentChangeOrderApiView):
    """Endpoint for changing the order of equipment up"""

    def change_order(self, equipment):
        print("Changing order up")
        equipment.up()


class EquipmentOrderDownApiView(EquipmentChangeOrderApiView):
    """Endpoint for changing the order of equipment up"""

    def change_order(self, equipment):
        print("Changing order down")
        equipment.down()
