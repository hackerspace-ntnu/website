from django.contrib import admin

from .models import DoorStatus, OpenData


@admin.register(DoorStatus)
class DoorStatusAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            "Status",
            {
                "fields": [
                    "name",
                    "datetime",
                    "status",
                ]
            },
        )
    ]
    search_fields = ["title"]


@admin.register(OpenData)
class OpenDataAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            "Data",
            {
                "fields": [
                    "opened",
                    "closed",
                ]
            },
        )
    ]
    search_fields = ["opened"]
