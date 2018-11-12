from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from flight.api.serializers import FlightSerializer, TicketSerializer
from flight.models import Flight, Ticket
from flight.permissions import IsOwner
from flight.tasks import notify_user_of_confirmed_ticket, notify_user_of_reservation
from flight.utils import convert_date_to_unix


# Create your views here.

class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        permission_classes = [IsAuthenticated, ]
        if self.action in ('create', 'destroy', 'update',
                           'partial_update', 'flight_status'):
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['patch'])
    def flight_status(self, request, pk=None):
        status = request.data.get('status')
        if not status:
            response = dict(message="Status field is required")
            return Response(response, status=400)

        if status not in (Flight.STATUSES):
            response = dict(message="Invalid flight status")
            return Response(response, status=400)

        queryset = Flight.objects.all()
        flight = get_object_or_404(queryset, pk=pk)

        flight.status = request.data.get('status')
        flight.save()
        serializer = FlightSerializer(flight)
        return Response(serializer.data, status=200)

    @action(detail=True, methods=['post'])
    def reserve(self, request, pk=None):
        user = request.user
        try:
            flight = Flight.objects.get(pk=pk)
        except Flight.DoesNotExist:
            response = dict(message="Flight not found")
            return Response(response, status=status.HTTP_404_NOT_FOUND)

        if Ticket.objects.filter(user=user, flight=flight).exists():
            return Response(dict(message="Ticket already exist for this flight"), status=409)

        ticket = Ticket.objects.create(
            user=user,
            flight=flight,
            arrival_time=flight.arrival_time,
            arrival_date=flight.arrival_date,
            departure_time=flight.departure_time,
            departure_date=flight.departure_date,
            departure_location=flight.departure_location,
            arrival_location=flight.arrival_location
        )
        ticket.save()
        # Run celery task to send email to customer of reserved ticket
        notify_user_of_reservation.delay(
            ticket.pk
        )
        serializer = TicketSerializer(ticket)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def book(self, request, pk=None):
        queryset = Flight.objects.all()
        flight = get_object_or_404(queryset, pk=pk)
        ticket = Ticket.objects.filter(user=request.user, flight=flight).exclude(
            status__in=(
                Ticket.RESERVED
            ))
        if ticket.exists():
            response = dict(
                message="A ticket has either been booked or confirmed for this flight"
            )
            return Response(response, status=400)

        ticket = Ticket.objects.create(
            user=request.user,
            flight=flight,
            arrival_time=flight.arrival_time,
            arrival_date=flight.arrival_date,
            departure_time=flight.departure_time,
            departure_date=flight.departure_date,
            departure_location=flight.departure_location,
            arrival_location=flight.arrival_location,
            status=Ticket.BOOKED
        )
        ticket.save()
        serializer = TicketSerializer(ticket)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'], url_path='reserved/(?P<date>[0-9_-]+)')
    def reserved(self, request, pk=None, date=None):
        queryset = Flight.objects.all()
        flight = get_object_or_404(queryset, pk=pk)

        reserved_tickets = flight.tickets.filter(
            status=Ticket.CONFIRMED,
        )
        date_to_timestamp = convert_date_to_unix(date)

        tickets = [
            ticket for ticket in reserved_tickets
            if convert_date_to_unix(ticket.created_at.strftime('%Y-%m-%d')) == date_to_timestamp
        ]

        serializer = TicketSerializer(tickets, many=True)
        response = {
            "reservations": serializer.data,
            "reservations_count": len(tickets)
        }
        return Response(response, status=status.HTTP_200_OK)


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def get_permissions(self):
        permission_classes = [IsAuthenticated, ]
        if self.action in ('create', 'list'):
            permission_classes = [IsAdminUser]
        if self.action in ('retrieve', 'destroy'):
            permission_classes = [IsOwner]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['patch'])
    def book(self, request, pk=None):
        queryset = Ticket.objects.all()
        ticket = get_object_or_404(queryset, pk=pk)

        if ticket.user != request.user:
            response = dict(message="You are not authorized to book this ticket")
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)

        if ticket.status in (Ticket.CONFIRMED, Ticket.BOOKED):
            response = dict(message="This ticket has either been booked or purchased")
            return Response(response, status=status.HTTP_403_FORBIDDEN)

        ticket.status = Ticket.BOOKED
        ticket.save()
        serializer = TicketSerializer(ticket)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def purchase(self, request, pk=None):
        current_user = request.user
        queryset = Ticket.objects.all()
        ticket = get_object_or_404(queryset, pk=pk)

        if ticket.user != current_user:
            response = dict(message="You are not authorized to purchase this ticket")
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)

        if ticket.status == Ticket.BOOKED:
            # run code for purchase ticket and send email to customer that ticket has been confirmed
            ticket.status = Ticket.CONFIRMED
            ticket.save()
            notify_user_of_confirmed_ticket.delay(
                ticket.pk
            )
            serializer = TicketSerializer(ticket)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(dict(message="Ticket has been purchased for this flight"), status=400)

    def update(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        queryset = Ticket.objects.all()
        ticket = get_object_or_404(queryset, pk=pk)

        if ticket.user != request.user:
            response = dict(message="You are not authorized to update this ticket")
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)

        if ticket.status in (Ticket.CONFIRMED, Ticket.BOOKED):
            response = dict(message="Cannot update a booked or confirmed ticket")
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        update_set = {'arrival_time', 'arrival_date', 'departure_time',
                      'departure_date', 'arrival_location', 'departure_location'}

        request_payload_set = set(request.data.keys())

        if request_payload_set.issubset(update_set):
            for key, value in request.data.items():
                setattr(ticket, key, value)

            ticket.save()
            serializer = TicketSerializer(ticket)
            return Response(serializer.data, status=status.HTTP_200_OK)

        response = dict(message="Some of the fields provided are not permitted for this action")
        return Response(response, status=400)
