from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin

from .models import Article, Event, Event_responsible, EventRegistration, Upload


class EventRegistrationInline(admin.TabularInline):
    model = Event_responsible
    extra = 1
    verbose_name = "Event responsible"
    verbose_name_plural = "Event responsible"


@admin.register(Event)
class Eventadmin(MarkdownxModelAdmin):
    fieldsets = [
        ("Article", {"fields": ["title", "main_content"]}),
        ("Ingress", {"fields": ["ingress_content"]}),
        (
            "Dates",
            {
                "fields": [
                    "time_start",
                    "time_end",
                ]
            },
        ),
        ("Place", {"fields": ["place", "place_href"]}),
        (
            "Registration",
            {
                "fields": [
                    "external_registration",
                    "registration",
                    "max_limit",
                    "registration_start",
                    "registration_end",
                    "deregistration_end",
                ]
            },
        ),
        ("Skills", {"fields": ["skills"]}),
        ("Advanced", {"fields": ["draft", "internal"]}),
    ]
    search_fields = ["title"]
    list_display = ["title", "pub_date", "draft", "internal"]
    inlines = [EventRegistrationInline]


@admin.register(Article)
class ArticleAdmin(MarkdownxModelAdmin):
    fieldsets = [
        ("Article", {"fields": ["title", "main_content"]}),
        ("Ingress", {"fields": ["ingress_content"]}),
        (
            "Thumbnail",
            {
                "fields": [
                    "thumbnail",
                ]
            },
        ),
        ("Advanced", {"fields": ["redirect", "internal", "draft"]}),
        (
            "Meta",
            {
                "fields": [
                    "views",
                ]
            },
        ),
    ]
    search_fields = ["title"]
    list_display = ["title", "pub_date", "draft", "internal"]


@admin.register(Upload)
class UploadModelAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            "Upload",
            {
                "fields": [
                    "title",
                    "file",
                ]
            },
        )
    ]
    search_fields = ["title"]


class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = [
        "__str__",
        "username",
        "event",
        "date",
    ]


admin.site.register(EventRegistration, EventRegistrationAdmin)
