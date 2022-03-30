from django.contrib import admin

from .models import Category, Profile, Skill, TermsOfService


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    search_fields = [
        "user__username",
        "user__first_name",
        "user__last_name",
        "user__email",
    ]
    list_filter = ["user__is_staff", "user__groups"]
    list_display = ["get_username", "get_first_name", "get_last_name"]

    @admin.display(description="brukernavn")
    def get_username(self, obj):
        return obj.user.username

    @admin.display(description="fornavn")
    def get_first_name(self, obj):
        return obj.user.first_name

    @admin.display(description="etternavn")
    def get_last_name(self, obj):
        return obj.user.last_name


admin.site.register(TermsOfService)
admin.site.register(Skill)
admin.site.register(Category)
