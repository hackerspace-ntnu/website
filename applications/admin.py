from django.contrib import admin
from .models import Application

class ApplicationAdmin(admin.ModelAdmin):
    list_display = [
        '__str__',
        'group_choice',
    ]

admin.site.register(Application, ApplicationAdmin)

