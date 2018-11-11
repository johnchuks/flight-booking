from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action

from flight.api.serializers import FlightSerializer, TicketSerializer
from flight.models import Flight, Ticket
from flight.permissions import IsOwner
# Create your views here.

class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        permission_classes = [IsAuthenticated,]
        if self.action in ('create', 'destroy', 'update', 'partial_update', 'flight_status'):
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
        ## Run celery task to send email to customer of reserved ticket
        serializer = TicketSerializer(ticket)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def get_permissions(self):
        permission_classes = [IsAuthenticated,]
        if self.action in ('create','list'):
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
            subject = "Your E-ticket Itinerary"
            context = dict(
                name=ticket.user.first_name,
                flight_number=ticket.flight.flight_number,
                arrival_time=ticket.arrival_time,
                arrival_date=ticket.arrival_date,
                departure_time=ticket.departure_time,
                departure_date=ticket.departure_date,
                departure_location=ticket.departure_location,
                arrival_location=ticket.arrival_location,
                ticket_reference='8NDRTGF'
            )
            from_email='services@airtech.co'
            to_email = 'johnboscoohia@gmail.com'
            ticket_info = get_template('email.txt').render(context)
            send_mail(subject, ticket_info, from_email, [to_email], fail_silently=True)

            serializer = TicketSerializer(ticket)
            return Response(serializer.data, status=status.HTTP_200_OK)


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
            ## Send email of ticket updated
            serializer = TicketSerializer(ticket)
            return Response(serializer.data, status=status.HTTP_200_OK)

        response = dict(message="Some of the fields provided are not permitted for this action")
        return Response(response, status=400)
