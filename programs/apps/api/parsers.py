"""
Custom DRF request parsers.  These can be used by views to handle different
content types, as specified by `<Parser>.media_type`.

To use these in an APIView, set `<View>.parser_classes` to a list including the
desired parsers.  See http://www.django-rest-framework.org/api-guide/parsers/
for details.
"""

from rest_framework.parsers import JSONParser


class MergePatchParser(JSONParser):
    """
    Custom parser to be used with the "merge patch" implementation (https://tools.ietf.org/html/rfc7396).
    """
    media_type = 'application/merge-patch+json'
