from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from flight.api.serializers import FlightSerializer
from flight.models import Flight 

# Create your views here.

class FlightViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminUser, )
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
