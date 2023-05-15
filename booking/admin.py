from django.contrib import admin
from booking.models import (Place, Event, Ticket, Profile, Purchase, Review)


class PlaceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


admin.site.register(Place, PlaceAdmin)
admin.site.register(Event)
admin.site.register(Ticket)
admin.site.register(Profile)
admin.site.register(Purchase)
admin.site.register(Review)
