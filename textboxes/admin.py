from django.contrib import admin

from textboxes.models import Textbox


@admin.register(Textbox)
class TextboxAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Textbox', {
            'fields': [
                'header_text',
                'text_text',
                'text_columns'
            ]
        }),
        (None, {
            'fields': [
                'pub_date'
            ]
        }),
        ('Custom header', {
            'fields': [
                'header_fontfamily',
                'header_fontsize',
                'header_color'
            ],
            'classes': [
                'collapse'
            ]
        }),
        ('Custom text', {
            'fields': [
                'text_fontfamily',
                'text_fontsize',
                'text_color'
            ], 'classes': [
                'collapse'
            ]
        }),
    ]
    search_fields = ['header_text']
