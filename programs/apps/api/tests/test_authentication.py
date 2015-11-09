"""
Tests for REST API Authentication
"""
import ddt
from django.contrib.auth.models import Group
from django.db import IntegrityError
from django.test import TestCase
import mock
from rest_framework.exceptions import AuthenticationFailed

from programs.apps.api.authentication import JwtAuthentication, pipeline_set_user_roles
from programs.apps.api.v1.tests.mixins import JwtMixin
from programs.apps.core.constants import Role
from programs.apps.core.models import User
from programs.apps.core.tests.factories import UserFactory


class TestJWTAuthentication(JwtMixin, TestCase):
    """
    Test id_token authentication used with the browseable API.
    """
    USERNAME = 'test-username'

    def test_no_preferred_username(self):
        """
        Ensure the service gracefully handles an inability to extract a username from the id token.
        """
        # with preferred_username: all good
        authentication = JwtAuthentication()
        user = authentication.authenticate_credentials({'preferred_username': self.USERNAME})
        self.assertEqual(user.username, self.USERNAME)

        # missing preferred_username: exception
        authentication = JwtAuthentication()
        with self.assertRaises(AuthenticationFailed):
            authentication.authenticate_credentials({})

    def test_user_creation_failure(self):
        """
        Verify that the service is robust to failures during user creation.
        """
        authentication = JwtAuthentication()

        with mock.patch.object(User.objects, 'get_or_create') as mocked:
            # If side_effect is an iterable, each call to the mock will return
            # the next value from the iterable.
            # See: https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock.side_effect.
            mocked.side_effect = [
                IntegrityError,
                (User.objects.create(username=self.USERNAME), False)
            ]

            user = authentication.authenticate_credentials({'preferred_username': self.USERNAME})
            self.assertEqual(user.username, self.USERNAME)


@ddt.ddt
class TestPipelineUserRoles(TestCase):
    """
    Ensure that user roles are set correctly based on a payload containing claims
    about the user, during login via social auth.
    """

    def setUp(self):
        self.user = UserFactory.create()
        super(TestPipelineUserRoles, self).setUp()

    def assert_has_admin_role(self, has_role=True):
        """
        Shorthand convenience.
        """
        _assert = self.assertTrue if has_role else self.assertFalse
        _assert(self.user.groups.filter(name=Role.ADMINS).exists())

    def assert_pipeline_result(self, result):
        """
        Shorthand convenience.  Ensures that the output of the pipeline function
        adheres to the social auth pipeline interface and won't break the auth flow.
        """
        self.assertEqual(result, {'user': self.user})

    def test_admin_role_is_assigned(self):
        """
        Make sure the user is assigned the ADMINS role if the "administrator" claim
        is set to true.
        """
        self.assert_has_admin_role(False)
        result = pipeline_set_user_roles({"administrator": True}, self.user)
        self.assert_has_admin_role()
        self.assert_pipeline_result(result)

    @ddt.data({"administrator": False}, {})
    def test_admin_role_is_unassigned(self, payload):
        """
        Make sure the user is unassigned from the ADMINS role, even if they previously
        had that role, if the "administrator" claim is not set to true.
        """
        self.user.groups.add(Group.objects.get(name=Role.ADMINS))  # pylint: disable=no-member
        self.assert_has_admin_role()
        result = pipeline_set_user_roles(payload, self.user)
        self.assert_has_admin_role(False)
        self.assert_pipeline_result(result)

    def test_no_user(self):
        """
        Make sure nothing breaks if the user wasn't authenticated or was otherwise
        popped somewhere along the pipeline.
        """
        result = pipeline_set_user_roles({}, None)
        self.assertEqual(result, {})
