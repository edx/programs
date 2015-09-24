"""
Tests for REST API Authentication
"""
from django.test import TestCase
from rest_framework.exceptions import AuthenticationFailed

from programs.apps.api.authentication import JwtAuthentication
from programs.apps.api.v1.tests.mixins import JwtMixin


class TestJWTAuthentication(JwtMixin, TestCase):
    """
    Test id_token authentication used with the browseable API.
    """

    def test_no_preferred_username(self):
        """
        Ensure the service gracefully handles an inability to extract a username from the id token.
        """
        # with preferred_username: all good
        authentication = JwtAuthentication()
        user = authentication.authenticate_credentials({'preferred_username': 'test-username'})
        self.assertEqual(user.username, 'test-username')

        # missing preferred_username: exception
        authentication = JwtAuthentication()
        with self.assertRaises(AuthenticationFailed):
            authentication.authenticate_credentials({})
