from django.contrib import admin
from booking.models import Movie,Concert, Theater, Seat

admin.site.register(Movie)
admin.site.register(Concert)
admin.site.register(Theater)
admin.site.register(Seat)

# Register your models here.
