"""Tests for Django Rest Framework Session Authentication package."""
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase


class SessionAuthViewTestCase(APITestCase):

    """Tests for functions on the SessionAuthView."""

    def setUp(self):
        """Create a test user."""
        self.username = 'test'
        self.email = 'test@test.com'
        self.password = 'test'
        self.user = User.objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password
        )

    def check_client_logged_out(self):
        """Utility function to check session auth logout worked."""
        self.assertEqual(len(self.client.session.items()), 0)

    def check_client_logged_in(self):
        """Utility function to check session auth login worked."""
        self.assertEqual(
            self.client.session['_auth_user_backend'],
            'django.contrib.auth.backends.ModelBackend'
        )
        self.assertEqual(
            self.client.session['_auth_user_id'],
            self.user.id
        )

        # Apparently _auth_user_hash is in 1.4 and 1.7, but not 1.6?
        # self.assertEqual(
        #     self.client.session['_auth_user_hash'],
        #     self.user.get_session_auth_hash()
        # )

    def test_session_login_json(self):
        """Test for correct login by posting credentials as JSON."""
        self.check_client_logged_out()

        response = self.client.post(
            '/auth-session/',
            {
                'username': self.username,
                'password': self.password
            },
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data,
            {
                'detail': 'Session login successful.'
            }
        )
        self.check_client_logged_in()

    def test_session_login_form(self):
        """Test for correct login by posting credentials as a form."""
        self.check_client_logged_out()

        response = self.client.post(
            '/auth-session/',
            {
                'username': self.username,
                'password': self.password
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data,
            {
                'detail': 'Session login successful.'
            }
        )
        self.check_client_logged_in()

    def test_session_login_no_credentials_json(self):
        """Test login fails when no credentials posted by JSON."""
        self.check_client_logged_out()

        response = self.client.post(
            '/auth-session/',
            None,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data,
            {
                'password': ['This field is required.'],
                'username': ['This field is required.']
            }
        )
        self.check_client_logged_out()

    def test_session_login_no_credentials_form(self):
        """Test login fails when no credentials posted by form."""
        self.check_client_logged_out()

        response = self.client.post(
            '/auth-session/',
            None
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data,
            {
                'password': ['This field is required.'],
                'username': ['This field is required.']
            }
        )
        self.check_client_logged_out()

    def test_session_login_bad_credentials_json(self):
        """Test login fails when bad credentials posted by JSON."""
        self.check_client_logged_out()

        response = self.client.post(
            '/auth-session/',
            {
                'username': 'wrong',
                'password': 'wrong'
            },
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data,
            {
                'non_field_errors': [
                    'Unable to log in with provided credentials.'
                ]
            }
        )
        self.check_client_logged_out()

    def test_session_login_bad_credentials_form(self):
        """Test login fails when bad credentials posted by form."""
        self.check_client_logged_out()

        response = self.client.post(
            '/auth-session/',
            {
                'username': 'wrong',
                'password': 'wrong'
            }
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data,
            {
                'non_field_errors': [
                    'Unable to log in with provided credentials.'
                ]
            }
        )
        self.check_client_logged_out()

    def test_session_login_inactive_user(self):
        """Check that an inactive user can't login."""
        self.check_client_logged_out()
        self.user.is_active = False
        self.user.save()

        response = self.client.post(
            '/auth-session/',
            {
                'username': self.username,
                'password': self.password
            }
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data,
            {
                'non_field_errors': [
                    'User account is disabled.'
                ]
            }
        )
        self.check_client_logged_out()

    def test_session_logout(self):
        """Test logout occurs when DELETE request sent."""
        self.client.post(
            '/auth-session/',
            {
                'username': self.username,
                'password': self.password
            }
        )
        self.check_client_logged_in()

        response = self.client.delete('/auth-session/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data,
            {
                'detail': 'Session logout successful.'
            }
        )
        self.check_client_logged_out()

    def test_session_logout_no_credentials(self):
        """Check logout still works even without login."""
        self.check_client_logged_out()

        response = self.client.delete('/auth-session/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data,
            {
                'detail': 'Session logout successful.'
            }
        )
        self.check_client_logged_out()

    def test_get(self):
        """Check GET request denied."""
        response = self.client.get('/auth-session/')
        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def test_put(self):
        """Check PUT request denied."""
        response = self.client.put(
            '/auth-session/',
            {
                'username': self.username,
                'password': self.password
            }
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED
        )
