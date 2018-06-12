from django.contrib import admin

from .models import KaffeKanne, KaffeData

admin.site.register(KaffeKanne)
admin.site.register(KaffeData)
