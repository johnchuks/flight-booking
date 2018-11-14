from __future__ import absolute_import, unicode_literals

from datetime import datetime, date

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import get_template

from account.models import User
from celery_app import app
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
    from_email = settings.AIRTECH_MAIL
    to_email = 'johnboscoohia@gmail.com'
    ticket_info = get_template('confirmed.txt').render(context)
    send_mail(subject, ticket_info, from_email, [to_email], fail_silently=True)


@shared_task()
def notify_user_of_reservation(ticket_id):
    try:
        reserved_ticket = Ticket.objects.get(pk=ticket_id)
    except Ticket.DoesNotExist: #pragma: no cover
        return

    subject = "Your Flight Reservation"
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
    to_mail = reserved_ticket.user.email
    reservation_info = get_template('reserved.txt').render(context)
    send_mail(subject, reservation_info, from_email, [to_mail], fail_silently=True)


@app.task
def send_reminder_to_travellers():
    now = datetime.now()
    current_year = int(now.strftime("%Y"))
    current_month = int(now.strftime("%m"))
    current_day = int(now.strftime("%d"))
    current_date = date(current_year, current_month, current_day)

    customers = User.objects.all()

    for customer in customers:
        tickets = Ticket.objects.filter(user=customer, status=Ticket.CONFIRMED)

        if tickets.exists():
            confirmed_ticket = tickets[0]
            departure_date = confirmed_ticket.departure_date
            departure_year = int(departure_date.strftime("%Y"))
            departure_month = int(departure_date.strftime("%m"))
            departure_day = int(departure_date.strftime("%d"))
            confirmed_departure_date = date(departure_year, departure_month, departure_day)

            delta = confirmed_departure_date - current_date
            number_of_days = delta.days

            if number_of_days <= 1:
                subject = "Reminder Event for Flight {0}".format(confirmed_ticket.flight.flight_number)
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
                from_email = settings.AIRTECH_MAIL
                to_mail = confirmed_ticket.user.email
                reservation_info = get_template('reminder.txt').render(context)
                send_mail(subject, reservation_info, from_email, [to_mail], fail_silently=True)
