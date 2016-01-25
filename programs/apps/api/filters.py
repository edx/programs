"""
Reusable queryset filters for the REST API.
"""
from rest_framework import filters

from programs.apps.core.constants import Role
from programs.apps.programs.constants import ProgramStatus


class ProgramStatusRoleFilterBackend(filters.BaseFilterBackend):
    """
    Depending on the group membership of the requesting user, filter program
    results according to their status:

      - ADMINS can see programs with any status other than 'deleted'
      - LEARNERS can see programs with any status other than 'deleted' or 'unpublished'
    """

    def filter_queryset(self, request, queryset, view):
        allowed_status = [ProgramStatus.ACTIVE, ProgramStatus.RETIRED]
        if request.user.groups.filter(name=Role.ADMINS).exists():
            allowed_status.append(ProgramStatus.UNPUBLISHED)
        return queryset.filter(status__in=allowed_status)


class ProgramCompletionFilterBackend(filters.BaseFilterBackend):
    """
    Only active and retired programs should be candidates for completion. Deleted
    and unpublished programs should not be candidates for completion.
    """

    def filter_queryset(self, request, queryset, view):
        allowed_status = [ProgramStatus.ACTIVE, ProgramStatus.RETIRED]
        return queryset.filter(status__in=allowed_status)


class BaseQueryFilterBackend(filters.BaseFilterBackend):
    """
    A reusable base class for filtering querysets based on a GET parameter.
    """
    query_parameter = None  # specify the query parameter name.
    lookup_filter = None  # specify the model lookup to filter upon, using the value of the query parameter.

    def filter_queryset(self, request, queryset, view):
        if request.method == 'GET' and self.query_parameter in request.query_params:
            filter_kwargs = {self.lookup_filter: request.query_params[self.query_parameter]}
            return queryset.filter(**filter_kwargs)
        else:
            return queryset


class ProgramStatusQueryFilterBackend(BaseQueryFilterBackend):
    """
    Allows for filtering programs by their status using a query string argument.
    """
    query_parameter = 'status'
    lookup_filter = 'status'


class ProgramOrgKeyFilterBackend(BaseQueryFilterBackend):
    """
    Allows for filtering program listings by an organization key query string argument.
    """
    query_parameter = 'organization'
    lookup_filter = 'organizations__key'  # match over m2m, thus 'organizations'


class CourseCodeOrgKeyFilterBackend(BaseQueryFilterBackend):
    """
    Allows for filtering course code listings by an organization key query string argument.
    """
    query_parameter = 'organization'
    lookup_filter = 'organization__key'
