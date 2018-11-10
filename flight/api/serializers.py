from rest_framework import serializers
from flight.models import Flight


class FlightSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Flight
        fields = ('id', 'title', 'arrival_location', 'departure_location', 'arrival_time', 'departure_time')
    

