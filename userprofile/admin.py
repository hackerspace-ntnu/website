from django.contrib import admin
from .models import Profile, Skill


class ProfileAdmin(admin.ModelAdmin):
    list_filter = (
        ('tos_accepted', admin.BooleanFieldListFilter),
    )

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Skill)
