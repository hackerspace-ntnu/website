from django.urls import path

from inventory.views.equipment import (
    EquipmentCreateView,
    EquipmentDeleteView,
    EquipmentEditView,
    EquipmentListView,
    EquipmentOrderDownApiView,
    EquipmentOrderUpApiView,
    EquipmentView,
)
from inventory.views.item import (
    InventoryListView,
    ItemCreateView,
    ItemDeleteView,
    ItemDetailView,
    ItemUpdateView,
)
from inventory.views.item_loan import (
    ItemLoanApplicationView,
    ItemLoanApproveView,
    ItemLoanDeclineView,
    ItemLoanDetailView,
    ItemLoanListView,
    ItemLoanReturnedView,
)

app_name = "inventory"

urlpatterns = [
    path("", InventoryListView.as_view(), name="inventory"),
    path("item/<int:pk>/", ItemDetailView.as_view(), name="item"),
    path("new/", ItemCreateView.as_view(), name="new"),
    path("edit/<int:pk>/", ItemUpdateView.as_view(), name="edit"),
    path("delete/<int:pk>/", ItemDeleteView.as_view(), name="delete"),
    path("loans/", ItemLoanListView.as_view(), name="loans"),
    path("loans/<int:pk>/", ItemLoanDetailView.as_view(), name="loan_application"),
    path(
        "loans/approve/<int:pk>/",
        ItemLoanApproveView.as_view(),
        name="loan_approve",
    ),
    path("loans/deny/<int:pk>/", ItemLoanDeclineView.as_view(), name="loan_deny"),
    path(
        "loans/returned/<int:pk>/",
        ItemLoanReturnedView.as_view(),
        name="loan_returned",
    ),
    path(
        "loans/apply/<int:pk>/",
        ItemLoanApplicationView.as_view(),
        name="loan_apply",
    ),
    path("equipment/", EquipmentListView.as_view(), name="equipment"),
    path("equipment/item/<int:pk>/", EquipmentView.as_view(), name="equipment_detail"),
    path("equipment/new/", EquipmentCreateView.as_view(), name="equipment_new"),
    path(
        "equipment/edit/<int:pk>/", EquipmentEditView.as_view(), name="equipment_edit"
    ),
    path(
        "equipment/delete/<int:pk>/",
        EquipmentDeleteView.as_view(),
        name="equipment_delete",
    ),
    path(
        "equipment/<int:pk>/up/",
        EquipmentOrderUpApiView.as_view(),
        name="equipment_order_up",
    ),
    path(
        "equipment/<int:pk>/down/",
        EquipmentOrderDownApiView.as_view(),
        name="equipment_order_down",
    ),
]
