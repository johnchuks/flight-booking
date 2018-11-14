# from django.test import TestCase
# from flight.tasks import notify_user_of_reservation, notify_user_of_confirmed_ticket, send_reminder_to_travellers
# from account.tests.factories import UserFactory
# from flight.tests.factories import TicketFactory, FlightFactory
# from unittest.mock import patch
# from django.template.loader import get_template
# from django.conf import settings
#
#
# class TestCeleryTasks(TestCase):
#
#     def setUp(self):
#         self.user = UserFactory(
#             email='john@test.com',
#             first_name='johnb'
#         )
#         flight = FlightFactory(
#             flight_number="BA-324",
#             arrival_location='lagos',
#             departure_location='benin'
#         )
#
#         self.ticket = TicketFactory(
#             user=self.user,
#             flight=flight,
#             arrival_location='lagos',
#             departure_location='benin',
#             departure_date="2018-11-14",
#             status="CONFIRMED",
#         )
#
#         # self.reservation_task = notify_user_of_reservation.delay(
#         #     self.ticket.pk
#         # )
#         # self.confirmation_task = notify_user_of_confirmed_ticket.delay(
#         #     self.ticket.pk
#         # )
#         # self.reservation_results = self.reservation_task.get()
#         # self.confirmation_results = self.confirmation_task.get()
#         #
#         # self.reminder_task = send_reminder_to_travellers.delay()
#         # self.reminder_results = self.reminder_task.get()
#
#     # def mock_send_mail(self, 'new ticket', 'This', from_email, [to_email], fail_silently=True):
#
#     @patch('django.core.mail.send_mail')
#     def test_notify_user_of_reservation_success(self, mock):
#         subject = "Your Flight Reservation"
#         template = get_template('reserved.txt')
#         # self.reservation_task = notify_user_of_reservation.delay(
#         #     self.ticket.pk
#         # )
#         response = notify_user_of_reservation(
#             self.ticket.pk
#         )
#         # self.assertTrue(mock.called, True)
#         mock.assert_called_once_with(subject, template, settings.AIRTECH_MAIL, self.user.email, fail_silently=True)
#
#
#     # def test_notify_user_of_confirmed_ticket_success(self):
#     #     self.assertEqual(self.confirmation_task.state, 'SUCCESS')
#     #
#     # def test_remind_users_of_schedule(self):
#     #     self.assertEqual(self.reminder_task.state, 'SUCCESS')
#     #
