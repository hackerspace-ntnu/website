from django.contrib import admin
from .models import Image, FileCategory

admin.site.register(FileCategory)

@admin.register(Image)
class IllustrationAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Image', {
            'fields': [
                'title',
                'img_category',
                'file',
            ]
        }),
        ('Meta', {
            'fields': [
                'time',
                'number',
            ]
        }),
    ]
    search_fields = [
        'title',
    ]
