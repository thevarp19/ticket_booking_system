from django.contrib import admin
from booking.models import (Place, Event, Ticket, User, Purchase)


class PlaceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


admin.site.register(Place, PlaceAdmin)
admin.site.register(Event)
admin.site.register(Ticket)
admin.site.register(User)
admin.site.register(Purchase)
