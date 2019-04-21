from django.contrib import admin
from django.contrib.admin import ModelAdmin

from reservations.models import Queue, Reservation


class ReservationAdmin(ModelAdmin):
    model = Reservation
    ordering = ('-start_date', '-start_time')


admin.site.register(Queue)
admin.site.register(Reservation, ReservationAdmin)
