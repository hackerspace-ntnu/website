from django.contrib import admin

from reservations.models import Queue, Reservation

admin.site.register(Queue)
admin.site.register(Reservation)
