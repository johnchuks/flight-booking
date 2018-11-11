from rest_framework import serializers
from flight.models import Flight, Ticket


class FlightSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Flight
        fields = ('id', 'flight_number', 'arrival_location',
                  'departure_location', 'arrival_time', 'departure_time',
                  'status', 'arrival_date', 'departure_date'
                  )

class TicketSerializer(serializers.ModelSerializer):
    flight = FlightSerializer()


    class Meta:
        model = Ticket
        fields = ('id', 'flight', 'user', 'arrival_location','arrival_time',
                  'departure_location', 'arrival_time', 'departure_time',
                  'arrival_date', 'departure_location', 'departure_date'
                  )