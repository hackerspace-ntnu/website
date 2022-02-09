from django.contrib import admin

from .models import Category, Profile, Skill, TermsOfService


class ProfileAdmin(admin.ModelAdmin):
    pass


admin.site.register(Profile, ProfileAdmin)
admin.site.register(TermsOfService)
admin.site.register(Skill)
admin.site.register(Category)
