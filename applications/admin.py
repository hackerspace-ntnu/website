from django.contrib import admin
from .models import Application, ApplicationGroup, ApplicationPeriod, ApplicationGroupChoice


@admin.register(
    ApplicationGroup,
    ApplicationPeriod,
    ApplicationGroupChoice
)
class BaseApplicationAdmin(admin.ModelAdmin):
    list_display = [
        '__str__',
    ]


class ApplicationGroupChoiceInline(admin.TabularInline):
    model = Application.group_choice.through
    ordering = ['priority']


@admin.register(Application)
class ApplicationAdmin(BaseApplicationAdmin):
    inlines = [
        ApplicationGroupChoiceInline
    ]
