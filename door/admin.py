from django.contrib import admin
from .models import DoorStatus

@admin.register(DoorStatus)
class DoorStatusAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Status', {
            'fields': [
                'name',
                'status',
            ]
        })
    ]
    search_fields = [
        'title'
    ]
