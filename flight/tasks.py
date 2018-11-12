from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import get_template
from django.conf import settings

from flight.models import Ticket


@shared_task()
def notify_user_of_confirmed_ticket(ticket_id):
    try:
        confirmed_ticket = Ticket.objects.get(pk=ticket_id)
    except Ticket.DoesNotExist:
        return

    subject = "Your E-ticket Itinerary"
    context = dict(
        name=confirmed_ticket.user.first_name,
        flight_number=confirmed_ticket.flight.flight_number,
        arrival_time=confirmed_ticket.arrival_time,
        arrival_date=confirmed_ticket.arrival_date,
        departure_time=confirmed_ticket.departure_time,
        departure_date=confirmed_ticket.departure_date,
        departure_location=confirmed_ticket.departure_location,
        arrival_location=confirmed_ticket.arrival_location,
        ticket_reference=confirmed_ticket.booking_reference
    )
    from_email = 'services@airtech.co'
    to_email = 'johnboscoohia@gmail.com'
    ticket_info = get_template('confirmed.txt').render(context)
    send_mail(subject, ticket_info, from_email, [to_email], fail_silently=True)


@shared_task()
def notify_user_of_reservation(ticket_id):
    try:
        reserved_ticket = Ticket.objects.get(pk=ticket_id)
    except Ticket.DoesNotExist:
        return

    subject  = "Your Flight Reservation"
    context = dict(
        name=reserved_ticket.user.first_name,
        flight_number=reserved_ticket.flight.flight_number,
        arrival_time=reserved_ticket.arrival_time,
        arrival_date=reserved_ticket.arrival_date,
        departure_time=reserved_ticket.departure_time,
        departure_date=reserved_ticket.departure_date,
        departure_location=reserved_ticket.departure_location,
        arrival_location=reserved_ticket.arrival_location
    )
    from_email = settings.AIRTECH_MAIL
    to_mail = 'chuk4shizzy@yahoo.com'
    reservation_info = get_template('reserved.txt').render(context)
    send_mail(subject, reservation_info, from_email, [to_mail], fail_silently=True)

