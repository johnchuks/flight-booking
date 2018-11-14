import factory

from flight.models import Flight, Ticket


class FlightFactory(factory.DjangoModelFactory):
    class Meta:
        model = Flight


class TicketFactory(factory.DjangoModelFactory):
    class Meta:
        model = Ticket
