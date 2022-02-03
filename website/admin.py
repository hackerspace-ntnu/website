from django.contrib import admin
from django.contrib.admin import EmptyFieldListFilter
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

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
