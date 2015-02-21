from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase


class SessionAuthViewTestCase(APITestCase):

    def setUp(self):
        self.username = 'test'
        self.email = 'test@test.com'
        self.password = 'test'
        self.user = User.objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password
        )

    def test_session_login_json(self):
        response = self.client.post(
            '/auth-session/',
            {
                'username': self.username,
                'password': self.password
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
