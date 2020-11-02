from django.contrib import admin
from .models import Item, ItemLoan

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Item', {
            'fields': [
                'name',
                'stock',
                'description',
                'thumbnail'
            ]
        }),
        ('Meta', {
            'fields': [
                'views',
            ]
        }),
    ]
    search_fields = [
        'name',
    ]

admin.site.register(ItemLoan)