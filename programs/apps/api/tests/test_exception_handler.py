"""
Tests for custom exception handling in the API.
"""

from django.conf.urls import url
from django.test import override_settings, TestCase
import mock
from rest_framework import exceptions, status
from rest_framework.test import APIClient
from rest_framework.views import APIView
from testfixtures import LogCapture


LOG_NAME = 'programs.apps.api.exception_handler'
LOG_LEVEL = 'INFO'
LOG_MSG_TEMPLATE = "raised_http_401: exc_type=u'{exc_type}', exc_detail=u'{exc_detail}'"


# make "/" map to a dummy view, that we can patch to raise various exceptions.
urlpatterns = [
    url(r'^$', APIView.as_view())
]


class Custom401Exception(exceptions.APIException):  # pylint:disable=missing-docstring
    status_code = status.HTTP_401_UNAUTHORIZED


class Custom400Exception(exceptions.APIException):  # pylint:disable=missing-docstring
    status_code = status.HTTP_400_BAD_REQUEST


@override_settings(ROOT_URLCONF='programs.apps.api.tests.test_exception_handler')
class TestAuthExceptionHandler(TestCase):
    """
    Ensure APIExceptions mapping to 401 responses are logged for diagnostic
    purposes.
    """

    def _check_response(self, expected_status, expected_type, expected_message):
        """
        DRY helper.
        """
        client = APIClient()
        with LogCapture() as lc:
            response = client.get('/')
            self.assertEqual(response.status_code, expected_status)
            if expected_status == 401:
                # check for the log message
                lc.check(
                    (LOG_NAME, LOG_LEVEL, LOG_MSG_TEMPLATE.format(
                        exc_type=expected_type,
                        exc_detail=expected_message,
                    )),
                )
            else:
                # nothing should be logged
                lc.check()

    @mock.patch('rest_framework.views.APIView.initial', side_effect=exceptions.AuthenticationFailed())
    def test_builtin_401(self, _mock_get_response):
        """
        Ensure we emit a log message when exceptions with a 401 status code get
        raised.
        """
        self._check_response(
            401,
            'rest_framework.exceptions.AuthenticationFailed',
            'Incorrect authentication credentials.'
        )

    @mock.patch('rest_framework.views.APIView.initial', side_effect=Custom401Exception("oops"))
    def test_custom_401(self, _mock_get_response):
        """
        Ensure we emit a log message when exceptions with a 401 status code get
        raised.
        """
        self._check_response(401, 'programs.apps.api.tests.test_exception_handler.Custom401Exception', 'oops')

    @mock.patch('rest_framework.views.APIView.initial', side_effect=Custom400Exception("d'oh!"))
    def test_other_status(self, _mock_get_response):
        """
        Ensure we don't emit a log message when other exceptions get raised.
        """
        self._check_response(400, None, None)
