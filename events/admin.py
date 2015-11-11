from django.contrib import admin

from events.models import Event, Image, Thumbnail


class ImageInline(admin.StackedInline):
    model = Image
    extra = 0


class ThumbnailInline(admin.StackedInline):
    model = Thumbnail
    max_num = 1
    extra = 0


@admin.register(Event)
class Eventadmin(admin.ModelAdmin):
    fieldsets = [
        ('Article', {
            'fields': [
                'header_text',
                'text_text'
            ]
        }),
        ('Ingress', {
            'fields': [
                'ingress_header_text',
                'ingress_text'
            ]
        }),
        ('Dates', {
            'fields': [
                'pub_date',
                'event_date'
            ]
        }),
        ('Place', {
            'fields': [
                'event_place',
                'event_place_href'
            ]
        }),
        ('Custom article header', {
            'fields': [
                'header_fontfamily',
                'header_fontsize',
                'header_color'
            ],
            'classes': [
                'collapse'
            ]
        }),
        ('Custom article text', {
            'fields': [
                'text_fontfamily',
                'text_fontsize',
                'text_color'
            ],
            'classes': [
                'collapse'
            ]
        }),
        ('Custom ingress header', {
            'fields': [
                'ingress_header_fontfamily',
                'ingress_header_fontsize',
                'ingress_header_color'
            ],
            'classes': [
                'collapse'
            ]
        }),
        ('Custom ingress text', {
            'fields': [
                'ingress_fontfamily',
                'ingress_fontsize',
                'ingress_color'
            ],
            'classes': [
                'collapse'
            ]
        }),
        ('Thumbnail', {
            'fields': [
                'thumbnail',
            ]
        })
    ]
    search_fields = [
        'header_text'
    ]
    inlines = [
        ImageInline
    ]


#@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Image', {
            'fields': [
                'image_title',
                'image_src',
                'image_customDimensions',
                'image_width',
                'image_height',
                'image_float'
            ]
        })
    ]
    search_fields = [
        'image_title'
    ]

@admin.register(Thumbnail)
class ThumbnailAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Thumbnail', {
            'fields': [
                'thumbnail_title',
                'thumbnail_src',
            ]
        })
    ]
    search_fields = [
        'thumbnail_title'
    ]