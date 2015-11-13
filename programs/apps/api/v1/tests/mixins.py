"""
Mixins for Programs API tests.
"""
from time import time

from django.conf import settings
from django.contrib.auth.models import Group
import jwt
from rest_framework.test import APIClient

from programs.apps.core.tests.factories import UserFactory


JWT_AUTH = 'JWT_AUTH'


class JwtMixin(object):
    """ Mixin with JWT-related helper functions. """

    JWT_SECRET_KEY = getattr(settings, JWT_AUTH)['JWT_SECRET_KEY']
    JWT_ISSUER = getattr(settings, JWT_AUTH)['JWT_ISSUER']
    JWT_AUDIENCE = getattr(settings, JWT_AUTH)['JWT_AUDIENCE']

    def generate_token(self, payload, secret=None):
        """Generate a JWT token with the provided payload."""
        secret = secret or self.JWT_SECRET_KEY
        token = jwt.encode(payload, secret)
        return token

    def generate_id_token(self, user, admin=False, ttl=1, **overrides):
        """Generate a JWT id_token that looks like the ones currently
        returned by the edx oidc provider."""

        payload = self.default_payload(user=user, admin=admin, ttl=ttl)
        payload.update(overrides)
        return self.generate_token(payload)

    def default_payload(self, user, admin=False, ttl=1):
        """Generate a bare payload, in case tests need to manipulate
        it directly before encoding."""
        now = int(time())

        return {
            "iss": self.JWT_ISSUER,
            "sub": user.pk,
            "aud": self.JWT_AUDIENCE,
            "nonce": "dummy-nonce",
            "exp": now + ttl,
            "iat": now,
            "preferred_username": user.username,
            "administrator": admin,
            "email": user.email,
            "locale": "en",
            "name": user.full_name,
            "given_name": "",
            "family_name": "",
        }


class AuthClientMixin(object):
    """
    Mixin useful for getting APIClient objects in tests.
    """

    def get_authenticated_client(self, role_name):
        """
        Helper for concisely obtaining a `rest_framework.test.APIClient` instance,
        authenticated with a user having some specific role.
        """
        # create a user with the specified role
        user = UserFactory.create()
        user.groups.add(Group.objects.get(name=role_name))  # pylint: disable=no-member

        # create an APIClient and force auth
        client = APIClient()
        client.force_authenticate(user)
        return client
