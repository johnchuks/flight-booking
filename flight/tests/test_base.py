from django.urls import reverse
from rest_framework.test import APITestCase, APIRequestFactory
from account.tests.factories import login_user, UserFactory
from flight.api.views import FlightViewSet
from flight.tests.factories import FlightFactory, TicketFactory
from flight.models import Flight, Ticket


class TestFlightViewSet(APITestCase):

    def setUp(self):
        self.admin = UserFactory(
            is_staff=True,
            email='jb@test.com',
            password='funky',
        )
        self.user = UserFactory(
            email='kris@mail.com',
            password='funky'
        )

        logged_in_admin = login_user(dict(email=self.admin.email, password='funky'))
        logged_in_user = login_user(dict(email=self.user.email, password='funky'))
        self.admin_token = logged_in_admin.data['token']
        self.user_token = logged_in_user.data['token']

        self.factory = APIRequestFactory()
        self.flight_payload = dict(
            flight_number="BA-34",
            arrival_location="paris",
            departure_location="lagos",
            departure_time="12:30pm",
            arrival_time="6:00am",
            arrival_date="2015-11-04",
            departure_date='2015-11-04',
            price=30000
        )

        self.flight = FlightFactory(
            flight_number="BA-3443",
            arrival_location="london",
            departure_location="lagos",
            departure_time="12:30pm",
            arrival_time="6:00am",
            arrival_date="2015-11-05",
            departure_date='2015-11-05',
            price=30000
        )

    def test_create_flight_success(self):

        url = reverse('flights-list')
        view = FlightViewSet.as_view(
            actions={
                'post': 'create'
            }
        )

        request = self.factory.post(url, data=self.flight_payload, HTTP_AUTHORIZATION='JWT {}'.format(
            self.admin_token))
        response = view(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['flight_number'], 'BA-34')
        self.assertEqual(response.data['arrival_location'], 'paris')
        self.assertEqual(response.data['departure_location'], 'lagos')
        self.assertEqual(response.data['status'], Flight.OPEN)


    def test_create_flight_non_admin_fail(self):
        url = reverse('flights-list')
        view = FlightViewSet.as_view(
            actions={
                'post': 'create'
            }
        )

        request = self.factory.post(url, data=self.flight_payload, HTTP_AUTHORIZATION='JWT {}'.format(
            self.user_token))
        response = view(request)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data['detail'], "You do not have permission to perform this action.")


    def test_update_flight_status_success(self):
        url = reverse('flights-flight-status', args=(self.flight.pk,))
        view = FlightViewSet.as_view(
            actions={
                'patch': 'flight_status'
            }
        )
        request = self.factory.patch(url, data=dict(status="LANDED"), HTTP_AUTHORIZATION='JWT {}'.format(
            self.admin_token))

        response = view(request, pk=self.flight.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['status'], Flight.LANDED)


    def test_update_flight_status_non_admin(self):
        url = reverse('flights-flight-status', args=(self.flight.pk,))
        view = FlightViewSet.as_view(
            actions={
                'patch': 'flight_status'
            }
        )
        request = self.factory.patch(url, data=dict(status="LANDED"), HTTP_AUTHORIZATION='JWT {}'.format(
            self.user_token))

        response = view(request, pk=self.flight.pk)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data['detail'], 'You do not have permission to perform this action.')

    def test_no_flight_status_fail(self):
        url = reverse('flights-flight-status', args=(self.flight.pk,))
        view = FlightViewSet.as_view(
            actions={
                'patch': 'flight_status'
            }
        )
        request = self.factory.patch(url, HTTP_AUTHORIZATION='JWT {}'.format(
            self.admin_token))
        response = view(request, pk=self.flight.pk)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['message'],'Status field is required')

    def test_incorrect_flight_status_fail(self):
        url = reverse('flights-flight-status', args=(self.flight.pk,))
        view = FlightViewSet.as_view(
            actions={
                'patch': 'flight_status'
            }
        )
        request = self.factory.patch(url, data=dict(status="EXPIRED"), HTTP_AUTHORIZATION='JWT {}'.format(
            self.admin_token))
        response = view(request, pk=self.flight.pk)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['message'],'Invalid flight status')


    def test_book_flight_success(self):
        url = reverse('flights-book', args=(self.flight.pk,))
        view = FlightViewSet.as_view(
            actions={
                'post': 'book'
            }
        )
        request = self.factory.post(url, HTTP_AUTHORIZATION='JWT {}'.format(
            self.user_token))

        response = view(request, pk=self.flight.pk)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['status'], Ticket.BOOKED)
        self.assertEqual(response.data['arrival_location'], 'london')
        self.assertEqual(response.data['departure_location'], 'lagos')

    def test_book_flight_for_booked_ticket_fail(self):
        TicketFactory(
            status=Ticket.BOOKED,
            flight=self.flight,
            user=self.user
        )

        url = reverse('flights-book', args=(self.flight.pk,))
        view = FlightViewSet.as_view(
            actions={
                'post': 'book'
            }
        )
        request = self.factory.post(url, HTTP_AUTHORIZATION='JWT {}'.format(
            self.user_token))

        response = view(request, pk=self.flight.pk)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['message'], 'A ticket has either been booked or confirmed for this flight')


    def test_reserve_ticket_success(self):
        url = reverse('flights-reserve', args=(self.flight.pk,))
        view = FlightViewSet.as_view(
            actions={
                'post': 'reserve'
            }
        )
        request = self.factory.post(url, HTTP_AUTHORIZATION='JWT {}'.format(
            self.user_token))

        response = view(request, pk=self.flight.pk)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['status'], Ticket.RESERVED)
        self.assertEqual(response.data['arrival_location'], 'london')
        self.assertEqual(response.data['departure_location'], 'lagos')

    def test_reserve_ticket_flight_not_exist(self):
        url = reverse('flights-reserve', args=(23,))
        view = FlightViewSet.as_view(
            actions={
                'post': 'reserve'
            }
        )
        request = self.factory.post(url, HTTP_AUTHORIZATION='JWT {}'.format(
            self.user_token))

        response = view(request, pk=23)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['message'], 'Flight not found')

    def test_reserve_ticket_already_exist(self):
        TicketFactory(
            status=Ticket.BOOKED,
            flight=self.flight,
            user=self.user
        )
        url = reverse('flights-reserve', args=(self.flight.pk,))
        view = FlightViewSet.as_view(
            actions={
                'post': 'reserve'
            }
        )
        request = self.factory.post(url, HTTP_AUTHORIZATION='JWT {}'.format(
            self.user_token))

        response = view(request, pk=self.flight.pk)
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.data['message'], 'Ticket already exist for this flight')


    def test_tickets_confirmed_for_flight_success(self):
        TicketFactory(
            status=Ticket.CONFIRMED,
            flight=self.flight,
            user=self.user
        )
        url = reverse('flights-reserved', args=(self.flight.pk, "2018-11-14"))
        view = FlightViewSet.as_view(
            actions={
                'post': 'reserved'
            }
        )
        request = self.factory.post(url, HTTP_AUTHORIZATION='JWT {}'.format(
            self.admin_token))

        response = view(request, pk=self.flight.pk, date="2018-11-14")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['reservations_count'], 1)


class TestTicketViewSet(APITestCase):

    def setUp(self):
        self.admin = UserFactory(
            is_staff=True,
            email='jb@test.com',
            password='funky',
        )
        self.user = UserFactory(
            email='kris@mail.com',
            password='funky'
        )

        logged_in_admin = login_user(dict(email=self.admin.email, password='funky'))
        logged_in_user = login_user(dict(email=self.user.email, password='funky'))
        self.admin_token = logged_in_admin.data['token']
        self.user_token = logged_in_user.data['token']

        self.factory = APIRequestFactory()
