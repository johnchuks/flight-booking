from django.contrib import admin
from flight.models import Flight

# Register your models here.
@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    model = Flight
    list_display = ['id', 'title', 'arrival_location', 'departure_location', 'arrival_time', 'departure_time']
