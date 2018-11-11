from django.db import models
from django.conf import settings
from djmoney.models.fields import MoneyField

from flight.mixins import FlightMixin


class Flight(FlightMixin):

    # Flight status
    DELAYED = 'DELAYED'
    ARRIVED = 'ARRIVED'
    CANCELLED = 'CANCELLED'
    OPEN = 'OPEN'
    DEPARTED = 'DEPARTED'
    LANDED = 'LANDED'

    STATUS = (
        (DELAYED, 'Delayed'),
        (ARRIVED, 'Arrived'),
        (CANCELLED, 'Cancelled'),
        (OPEN, 'Open'),
        (DEPARTED, 'Departed'),
        (LANDED, 'Landed'),
    )

    STATUSES = (
        DEPARTED,
        DELAYED,
        CANCELLED,
        OPEN,
        LANDED,
        ARRIVED
    )

    flight_number = models.CharField(max_length=255, blank=False)
    status = models.CharField(max_length=50, choices=STATUS, default=OPEN)
    price = MoneyField(max_digits=14, decimal_places=2, default_currency='NGN')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    


class Ticket(FlightMixin):

    # Ticket Status
    RESERVED = 'RESERVED'
    BOOKED = 'BOOKED'
    CONFIRMED = 'CONFIRMED'

    STATUS = (
        (RESERVED, 'Reserved'),
        (BOOKED, 'Booked'),
        (CONFIRMED, 'Confirmed'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    flight = models.ForeignKey('flight.Flight', on_delete=models.CASCADE, related_name="tickets")
    status = models.CharField(max_length=50, choices=STATUS, default=RESERVED)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
