"""
Custom exception handling for API Views.
"""
import logging

from rest_framework.exceptions import APIException
from rest_framework.status import HTTP_401_UNAUTHORIZED
from rest_framework.views import exception_handler


logger = logging.getLogger(__name__)


def auth_exception_handler(exc, context):
    """
    Wrap default exception handling with diagnostic logging for auth failures.
    """
    if isinstance(exc, APIException) and exc.status_code == HTTP_401_UNAUTHORIZED:
        exc_type = u'{}.{}'.format(exc.__class__.__module__, exc.__class__.__name__)
        logger.info("raised_http_401: exc_type=%r, exc_detail=%r", exc_type, exc.detail)

    return exception_handler(exc, context)
