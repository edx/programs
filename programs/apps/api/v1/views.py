"""
Programs API views (v1).
"""
from rest_framework import mixins, viewsets
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated

from programs.apps.programs.constants import ProgramStatus
from programs.apps.programs.models import Program
from programs.apps.api.serializers import ProgramSerializer


class ProgramsViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """

    **Use Cases**

        List existing Programs, and create new ones.

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

    **Response Values**

        * id: The ID of the program.
        * name: The user-facing display name for this Program.
        * description: A full-length description of the Program.
        * category: The category / type of Program.  Right now the only value allowed is 'xseries'.
        * status: The lifecycle status of this Program.  Right now the only value allowed is 'unpublished'.
        * created: The date/time this Program was created.
        * modified: The date/time this Program was last modified.

    """
    permission_classes = (IsAuthenticated, DjangoModelPermissions)
    queryset = Program.objects.exclude(status=ProgramStatus.DELETED)
    serializer_class = ProgramSerializer
