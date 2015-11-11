"""
Programs API views (v1).
"""
from rest_framework import mixins, viewsets, parsers as drf_parsers

from programs.apps.programs import models
from programs.apps.api import filters, permissions, serializers, parsers as edx_parsers


class ProgramsViewSet(
        mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
        viewsets.GenericViewSet):
    """

    **Use Cases**

        List and update existing Programs, and create new ones.

    **Example Requests**

        # Return a list of programs in the system.
        GET /api/v1/programs/

        If the request is successful, the HTTP status will be 200 and the response body will
        contain a JSON-formatted array of programs.

        # Create a new program.
        POST /api/v1/programs/

        If the request is successful, the HTTP status will be 201 and the response body will
        contain a JSON-formatted representation of the newly-created program.

        Only users with global administrative rights may create programs.  POST requests from non-
        admins will result in status 403.

        # Update existing Program.
        PATCH /api/v1/programs/{program_id}

        If the request is successful, the HTTP status will be 200 and the response body will
        contain a JSON-formatted representation of the newly-updated program.

        Only users with global administrative rights may update programs.  PATCH requests from non-
        admins will result in status 403.

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
    permission_classes = (permissions.IsAdminGroupOrReadOnly, )
    queryset = models.Program.objects.all()
    filter_backends = (
        filters.ProgramStatusRoleFilterBackend,
        filters.ProgramStatusQueryFilterBackend,
        filters.ProgramOrgKeyFilterBackend,
    )
    serializer_class = serializers.ProgramSerializer
    parser_classes = (edx_parsers.MergePatchParser, drf_parsers.JSONParser)


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
    permission_classes = (permissions.IsAdminGroup, )
    queryset = models.CourseCode.objects.all()
    serializer_class = serializers.CourseCodeSerializer
    filter_backends = (filters.CourseCodeOrgKeyFilterBackend, )


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
    permission_classes = (permissions.IsAdminGroup, )
    queryset = models.Organization.objects.all()
    serializer_class = serializers.OrganizationSerializer
