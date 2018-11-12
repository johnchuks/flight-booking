from rest_framework import serializers

from flight.models import Flight, Ticket


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = ('id', 'flight_number', 'arrival_location',
                  'departure_location', 'arrival_time', 'departure_time',
                  'status', 'arrival_date', 'departure_date'
                  )


class LimitedFlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = ('id', 'flight_number', 'status')


class TicketSerializer(serializers.ModelSerializer):
    flight = LimitedFlightSerializer(read_only=True)

    class Meta:
        model = Ticket
        fields = ('id', 'flight', 'booking_reference', 'status', 'user', 'arrival_location', 'arrival_time',
                  'departure_location', 'arrival_time', 'departure_time',
                  'arrival_date', 'departure_location', 'departure_date'
                  )
