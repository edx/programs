"""
Programs API views (v1).
"""
from django.db import transaction
from django.db.models import Prefetch
from django.db.models.functions import Lower
from django.utils.decorators import method_decorator
from rest_framework import (
    mixins,
    parsers as drf_parsers,
    viewsets,
)

from programs.apps.programs import models
from programs.apps.api import (
    filters,
    parsers as edx_parsers,
    permissions as edx_permissions,
    serializers,
)


class ProgramsViewSet(
        mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
        viewsets.GenericViewSet):
    """

    **Use Cases**

        List and update existing Programs, create new Programs, and find completed Programs.

    **Example Requests**

        # Return a list of programs in the system.
        GET /api/v1/programs/

        If the request is successful, the HTTP status will be 200 and the response body will
        contain a JSON-formatted array of programs.

        # Create a new program.
        POST /api/v1/programs/

        If the request is successful, the HTTP status will be 201 and the response body will
        contain a JSON-formatted representation of the newly-created program.

        Only users with global administrative rights may create programs. POST requests from non-
        admins will result in status 403.

        # Update existing Program.
        PATCH /api/v1/programs/{program_id}

        If the request is successful, the HTTP status will be 200 and the response body will
        contain a JSON-formatted representation of the newly-updated program.

        Only users with global administrative rights may update programs. PATCH requests from non-
        admins will result in status 403.

        # Find completed programs.
        POST /api/v1/programs/complete/

        Request body must include a serialized representation of completed course runs, including
        the modes in which the runs were completed. Expected to be of the form:

        {'completed_courses': [
            {'course_id': 'foo', 'mode': 'bar'},
            ...
            {'course_id': 'baz', 'mode': 'qux'}
        ]}

        If the request is successful, the HTTP status will be 200 and the response body will
        include JSON containing the IDs of the completed programs.

    **Response Values**

        * id: The ID of the program.
        * name: The user-facing display name for this Program.
        * subtitle: A brief, descriptive subtitle for the Program.
        * category: The category / type of Program.  Right now the only value allowed is 'xseries'.
        * status: The lifecycle status of this Program.  Right now the only value allowed is 'unpublished'.
        * marketing_slug: Slug used to generate links to the marketing site.
        * organizations: List data containing organizations with which the program is associated.
        * created: The date/time this Program was created.
        * modified: The date/time this Program was last modified.

    """
    permission_classes = (edx_permissions.IsAdminGroupOrReadOnly, )
    filter_backends = (
        filters.ProgramStatusRoleFilterBackend,
        filters.ProgramStatusQueryFilterBackend,
        filters.ProgramOrgKeyFilterBackend,
    )
    serializer_class = serializers.ProgramSerializer
    parser_classes = (edx_parsers.MergePatchParser, drf_parsers.JSONParser)

    @method_decorator(transaction.non_atomic_requests)
    def dispatch(self, request, *args, **kwargs):
        return super(ProgramsViewSet, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """Perform eager loading of data to prevent a cascade of performance-degrading queries."""
        queryset = models.Program.objects.all()

        # Database queries which have already been run are never updated automatically
        # by the Django ORM. As a result, updates to prefetched related objects are not
        # reflected in responses.
        # See: https://github.com/tomchristie/django-rest-framework/issues/2442.
        if self.request.method != 'GET':
            return queryset

        return queryset.prefetch_related(
            Prefetch(
                'programorganization_set',
                queryset=models.ProgramOrganization.objects.select_related('organization')
            ),
            Prefetch(
                'programcoursecode_set',
                queryset=models.ProgramCourseCode.objects.select_related()
            ),
            'programcoursecode_set__run_modes',
        )


class CourseCodesViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """

    **Use Cases**

        List existing course codes.  This action is only available to ADMIN users
        as part of building programs through an admin UX.

    **Example Requests**

        # Return a list of course codes in the system.
        GET /api/v1/course_codes/

        If the request is successful, the HTTP status will be 200 and the response body will
        contain a JSON-formatted array of course codes.

    **Response Values**

        * key: the prefix from the edX CourseKey, consisting of the "org" and "course" parts.
        * display_name: the display title of the course (derived from its LMS runs).
        * organization: The organization that is associated with this course code's runs in the LMS.
            * key: the prefix from the edX CourseKey, consisting of the "org" part.
            * display_name: the display title of the organization.

    """
    permission_classes = (edx_permissions.IsAdminGroup, )
    serializer_class = serializers.CourseCodeSerializer
    filter_backends = (filters.CourseCodeOrgKeyFilterBackend, )

    def get_queryset(self):
        """Perform eager loading of data to prevent a cascade of performance-degrading queries."""
        queryset = models.CourseCode.objects.all()

        return queryset.select_related('organization')


class OrganizationsViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """

    **Use Cases**

        List existing organizations.  This action is only available to ADMIN users
        as part of building programs through an admin UX.

    **Example Requests**

        # Return a list of organizations in the system.
        GET /api/v1/organizations/

        If the request is successful, the HTTP status will be 200 and the response body will
        contain a JSON-formatted array of organizations.

    **Response Values**

        * key: the prefix from the edX CourseKey, consisting of the "org" part.
        * display_name: the display title of the organization.

    """
    permission_classes = (edx_permissions.IsAdminGroup, )
    queryset = models.Organization.objects.all().order_by(Lower('key'))
    serializer_class = serializers.OrganizationSerializer
