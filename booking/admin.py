from django.contrib import admin
from booking.models import (Cinema, Ticket, User, Movie, Purchase)


class CinemaAdmin(admin.ModelAdmin):
    list_display = ('id', 'cinema_name')


admin.site.register(Cinema, CinemaAdmin)
admin.site.register(Ticket)
admin.site.register(User)
admin.site.register(Movie)
admin.site.register(Purchase)
