"""
Reusable pagination for REST API views.
"""
from rest_framework.response import Response
from rest_framework import pagination


class DefaultPagination(pagination.PageNumberPagination):
    """
    Default paginator for APIs in edx-platform.

    This has been copied from edx-platform/openedx/core/lib/api/paginators.py
    """
    page_size_query_param = "page_size"

    def get_paginated_response(self, data):
        """
        Annotate the response with pagination information.
        """
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'num_pages': self.page.paginator.num_pages,
            'results': data
        })
