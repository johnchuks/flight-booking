from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import get_template

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
        ticket_reference='8NDRTGF'
    )
    from_email = 'services@airtech.co'
    to_email = 'johnboscoohia@gmail.com'
    ticket_info = get_template('email.txt').render(context)
    send_mail(subject, ticket_info, from_email, [to_email], fail_silently=True)