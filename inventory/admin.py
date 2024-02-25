from django.contrib import admin
from ordered_model.admin import OrderedModelAdmin

from inventory.models.equipment import Equipment
from inventory.models.item import Item
from inventory.models.item_loan import ItemLoan


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            "Item",
            {
                "fields": [
                    "name",
                    "stock",
                    "unknown_stock",
                    "description",
                    "thumbnail",
                    "location",
                    "can_loan",
                    "max_loan_duration",
                ]
            },
        ),
        (
            "Meta",
            {
                "fields": [
                    "views",
                ]
            },
        ),
    ]
    search_fields = [
        "name",
    ]


@admin.register(ItemLoan)
class ItemLoanAdmin(admin.ModelAdmin):
    autocomplete_fields = ["approver"]


@admin.register(Equipment)
class EquipmentAdmin(OrderedModelAdmin):
    list_display = ["name", "inventory_link", "move_up_down_links"]
