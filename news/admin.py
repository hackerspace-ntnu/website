from django.contrib import admin

from .models import Article, Event, Thumbnail, Upload


class ThumbnailInline(admin.StackedInline):
    model = Thumbnail
    max_num = 1
    extra = 0


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
                'pub_date',
                'date'
            ]
        }),
        ('Place', {
            'fields': [
                'place',
                'place_href'
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
        (None, {
            'fields': [
                'pub_date'
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


@admin.register(Thumbnail)
class ThumbnailAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Thumbnail', {
            'fields': [
                'title',
                'image',
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
