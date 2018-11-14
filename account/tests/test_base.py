import json
import os

from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.test import APITestCase, APIRequestFactory

from account.api.views import AirtechUserViewSet
from account.models import User
from account.tests.factories import login_user, UserFactory

client = Client()


class TestUserSignup(TestCase):
    def setUp(self):
        self.user_payload = {
            "first_name": 'lorem',
            "last_name": 'ipsum',
            "email": 'ipsum@gmail.com',
            "password": "lorem"
        }

        self.invalid_payload = {
            "last_name": 'wells',
            "password": "wells"
        }

    def test_successful_signup(self):
        url = reverse('sign_up')
        response = client.post(url,
                               data=json.dumps(self.user_payload),
                               content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'ipsum@gmail.com')

    def test_unsuccessful_signup(self):
        url = reverse('sign_up')
        response = client.post(url, data=json.dumps(self.invalid_payload),
                               content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['message'], 'email, password and firstname are required')


class TestUserLogin(APITestCase):
    def setUp(self):
        self.user = UserFactory(
            first_name='lorem',
            last_name='ipsum',
            email='ipsum@test.com',
            password='funky'
        )
        self.url = reverse('login')

    def test_successful_login(self):
        url = reverse('login')
        login_payload = dict(
            email=self.user.email,
            password="funky"
        )
        response = self.client.post(url, data=json.dumps(login_payload),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['email'], 'ipsum@test.com')

    def test_unsuccessful_login(self):
        invalid_payload = {
            'email': 're@gf.com',
            'password': 'lorem'
        }
        response = client.post(self.url, data=json.dumps(invalid_payload),
                               content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['message'], 'Invalid request')


class TestAirtechUser(APITestCase):
    def setUp(self):
        self.user1 = UserFactory(
            first_name='john',
            last_name='james',
            email='james@test.com',
            password='lorem',
            is_staff=True
        )
        self.user2 = UserFactory(
            first_name='john',
            last_name='ram',
            email='ram@test.com',
            password='lorem',
        )
        self.user3 = UserFactory(
            first_name='mark',
            last_name='ram',
            email='mark@test.com',
            password='lorem2',
        )
        valid_payload = {
            "email": 'james@test.com',
            "password": 'lorem'
        }
        self.factory = APIRequestFactory()

        self.admin = login_user(valid_payload)
        self.non_admin = login_user(dict(email=self.user2.email, password="lorem"))

    def test_list_all_users_admin(self):
        url = reverse('users-list')
        view = AirtechUserViewSet.as_view(
            actions={
                'get': 'list',
            }
        )
        request = self.factory.get(url, HTTP_AUTHORIZATION='JWT {}'.format(
            self.admin.data['token']))
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['first_name'], 'john')
        self.assertEqual(response.data[0]['email'], 'james@test.com')

    def test_list_users_not_admin(self):
        url = reverse('users-list')
        view = AirtechUserViewSet.as_view(
            actions={
                'get': 'list',
            }
        )
        request = self.factory.get(url, HTTP_AUTHORIZATION='JWT {}'.format(
            self.non_admin.data['token']))
        response = view(request)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['message'], 'You are not authorized to view this information')

    def test_get_user_by_id(self):
        url = reverse('users-detail', args=(self.user3.pk,))
        view = AirtechUserViewSet.as_view(
            actions={
                'get': 'retrieve',
            }
        )
        request = self.factory.get(url, HTTP_AUTHORIZATION='JWT {}'.format(
            self.admin.data['token']))

        response = view(request, pk=self.user3.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['first_name'], 'mark')
        self.assertEqual(response.data['email'], 'mark@test.com')

    def test_successful_user_update(self):
        url = reverse('users-detail', args=(self.user2.pk,))
        view = AirtechUserViewSet.as_view(
            actions={
                'put': 'update'
            }
        )
        request = self.factory.put(url, data=dict(first_name='johnbosco'), HTTP_AUTHORIZATION='JWT {}'.format(
            self.non_admin.data['token']))
        response = view(request, pk=str(self.user2.pk))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['first_name'], 'johnbosco')

    def test_unsuccessful_user_update(self):
        url = reverse('users-detail', args=(self.user3.pk,))
        view = AirtechUserViewSet.as_view(
            actions={
                'put': 'update'
            }
        )
        request = self.factory.put(url, data=dict(first_name='james'), HTTP_AUTHORIZATION='JWT {}'.format(
            self.non_admin.data['token']))
        response = view(request, pk=str(self.user3.pk))
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['message'], 'You are not authorized to edit this information')

    def test_unsuccessful_user_update_disallowed_field(self):
        url = reverse('users-detail', args=(self.user2.pk,))
        view = AirtechUserViewSet.as_view(
            actions={
                'put': 'update'
            }
        )
        request = self.factory.put(url, data=dict(email='john@bosco.co'), HTTP_AUTHORIZATION='JWT {}'.format(
            self.non_admin.data['token']))
        response = view(request, pk=str(self.user2.pk))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['message'], 'Some of the fields provided are not permitted for this action')

    def test_photo_upload_success(self):
        url = reverse('users-upload')
        view = AirtechUserViewSet.as_view(
            actions={
                'put': 'upload'
            }
        )
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        image = os.path.join(base_dir, 'account_photos/photo1.jpg')

        request = self.factory.put(url, data=dict(file=image), HTTP_AUTHORIZATION='JWT {}'.format(
            self.non_admin.data['token']))
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_delete_photo_success(self):
        url = reverse('users-delete-photo')
        view = AirtechUserViewSet.as_view(
            actions={
                'delete': 'delete_photo'
            }
        )
        request = self.factory.delete(url, HTTP_AUTHORIZATION='JWT {}'.format(
            self.non_admin.data['token']))

        response = view(request)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.data['message'], 'Photo deleted successfully')
