from django.contrib import admin

from flight.models import Flight, Ticket


# Register your models here.
@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    model = Flight
    list_display = ['id', 'flight_number', 'arrival_time',
                    'arrival_date', 'departure_date',
                    'departure_time', 'arrival_location', 'departure_location', 'price', 'status']


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    model = Ticket
    list_display = ['id', 'arrival_time', 'arrival_date', 'departure_date',
                    'departure_time', 'arrival_location', 'departure_location', 'status']
