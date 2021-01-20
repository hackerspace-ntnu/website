from django.contrib import admin

from .models import Article, Event, Upload, EventRegistration


@admin.register(Event)
class Eventadmin(admin.ModelAdmin):
    fieldsets = [
        ('Article', {
            'fields': [
                'title',
                'main_content'
            ]
        }),
        ('Ingress', {
            'fields': [
                'ingress_content'
            ]
        }),
        ('Dates', {
            'fields': [
                'time_start',
                'time_end',
            ]
        }),
        ('Place', {
            'fields': [
                'place',
                'place_href'
            ]
        }),
        ('Registration', {
            'fields': [
                'external_registration',
                'registration',
                'max_limit',
                'registration_start',
                'deregistration_end',
            ]
        }),
    ]
    search_fields = [
        'title'
    ]


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Article', {
            'fields': [
                'title',
                'main_content'
            ]
        }),
        ('Ingress', {
            'fields': [
                'ingress_content'
            ]
        }),
        ('Thumbnail', {
            'fields': [
                'thumbnail',
            ]
        }),
        ('Advanced', {
            'fields': [
                'redirect',
                'internal',
                'draft'
            ]
        }),
    ]
    search_fields = [
        'title'
    ]


@admin.register(Upload)
class UploadModelAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Upload', {
            'fields': [
                'title',
                'file',
            ]
        })
    ]
    search_fields = [
        'title'
    ]

class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = [
        '__str__',
        'username',
        'event',
        'date',
    ]

admin.site.register(EventRegistration, EventRegistrationAdmin)
