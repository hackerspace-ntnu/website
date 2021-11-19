from django.contrib import admin

from .models import Committee


class CommitteeAdmin(admin.ModelAdmin):
    autocomplete_fields = ["main_lead", "second_lead", "economy"]


admin.site.register(Committee, CommitteeAdmin)
