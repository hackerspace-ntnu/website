from django.contrib import admin

# Register your models here.
from internal.models import TimeTable, TimeTableSlotSignup

admin.site.register(TimeTable)
admin.site.register(TimeTableSlotSignup)
