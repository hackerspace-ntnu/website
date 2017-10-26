from django.contrib import admin
from .models import Profile, Skill,DutyTime,Group
# Register your models here.

admin.site.register(Skill)
admin.site.register(Profile)
admin.site.register(DutyTime)
admin.site.register(Group)
