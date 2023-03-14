from django.contrib import admin

from .models import Item, ItemCategory, ItemLoan


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
                    "category",
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


class ItemLoanAdmin(admin.ModelAdmin):
    autocomplete_fields = ["approver"]


admin.site.register(ItemLoan, ItemLoanAdmin)
admin.site.register(ItemCategory)
