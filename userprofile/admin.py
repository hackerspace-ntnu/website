from django.contrib import admin
from django.db import models
from django import forms
from .models import Profile, Skill, TermsOfService


class ProfileAdmin(admin.ModelAdmin):
    pass

admin.site.register(Profile, ProfileAdmin)
admin.site.register(TermsOfService)
admin.site.register(Skill)
