from django.contrib import admin
from django.contrib.admin import EmptyFieldListFilter
from django.contrib.admin.models import DELETION, LogEntry
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.html import escape
from django.utils.safestring import mark_safe

from .models import Banner, Card, FaqQuestion, Rule


class WatchlistFilter(EmptyFieldListFilter):
    def __init__(self, field, request, params, model, model_admin, field_path):
        super().__init__(field, request, params, model, model_admin, field_path)
        self.title = "vaktliste"

    def choices(self, changelist):
        for lookup, title in (
            (None, "Alle"),
            ("0", "På vaktliste"),
            ("1", "Ikke på vaktliste"),
        ):
            yield {
                "selected": self.lookup_val == lookup,
                "query_string": changelist.get_query_string(
                    {self.lookup_kwarg: lookup}
                ),
                "display": title,
            }


class CustomUserAdmin(UserAdmin):
    list_filter = UserAdmin.list_filter + (("watches", WatchlistFilter),)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Card)
admin.site.register(FaqQuestion)
admin.site.register(Rule)
admin.site.register(Banner)


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    actions = None

    date_hierarchy = "action_time"

    list_filter = ["user", "content_type", "action_flag"]

    search_fields = ["action_time", "object_repr", "change_message"]

    list_display = [
        "action_time",
        "user",
        "content_type",
        "object_link",
        "action_flag",
    ]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        if "admin/logentry" in request.path:
            return False
        return True

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    def object_link(self, obj):
        if obj.action_flag == DELETION:
            link = escape(obj.object_repr)
        else:
            ct = obj.content_type
            link = '<a href="%s">%s</a>' % (
                reverse(
                    "admin:%s_%s_change" % (ct.app_label, ct.model),
                    args=[obj.object_id],
                ),
                escape(obj.object_repr),
            )
        return mark_safe(link)

    object_link.admin_order_field = "object_repr"
    object_link.short_description = "object"
