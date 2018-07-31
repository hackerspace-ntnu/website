from django.contrib import admin
from .models import Application, ApplicationGroup

class ApplicationAdmin(admin.ModelAdmin):
    list_display = [
        '__str__',
    ]

admin.site.register(Application, ApplicationAdmin)
admin.site.register(ApplicationGroup, ApplicationAdmin)
