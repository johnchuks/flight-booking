import pytest
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.test import APITestCase
from account.models import User
from account.tests.factories import login_user, UserFactory
import json


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
        print(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['message'], 'email, password and firstname are required')


class TestUserLogin(APITestCase):

    def setUp(self):
        self.user = UserFactory(
            first_name='lorem',
            last_name='ipsum',
            email='ipsum@test.com',
            password="funky"
        )
        self.url = reverse('login')

    def test_successful_login(self):
        url = reverse('login')
        login_payload = dict(
                email=self.user.email,
                password=self.user.password
        )
        response = self.client.post(url, data=json.dumps(login_payload),
                               content_type='application/json', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['email'], 'ipsum@gmail.com')


    def test_unsuccessful_login(self):
        invalid_payload = {
            'email': 're@gf.com',
            'password': 'lorem'
        }
        response = client.post(self.url, data=json.dumps(invalid_payload),
                               content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['message'], 'Invalid request')


# class TestAirtechUser(APITestCase):
#
#     def setUp(self):
#         self.user1 = UserFactory(
#             first_name='john',
#             last_name='james',
#             email='james@test.com',
#             password='lorem',
#             is_staff=True
#         )
#         valid_payload = {
#             "email": 'james@test.com',
#             "password": 'lorem'
#         }
#         self.admin = login_user(valid_payload)
#         print(self.admin.data, 'Loginnnnnnismessedupooooooooo')
#     def test_list_all_users_admin(self):
#         # self.client.credentials(HTTP_AUTHORIZATION='JWT {}'.format(
#         #     self.admin.data['token']))
#         url = reverse('users')
#         response = self.client.get(url, content_type='application/json')
#         print(response.data, '=====>>>>>>')
#         self.assertEqual(response.status_code, 200)
