from django.contrib import admin

from .models import Article, Event, Upload


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
        })
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
