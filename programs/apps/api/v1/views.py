"""
Programs API views (v1).
"""
from rest_framework import mixins, viewsets

from programs.apps.programs.constants import ProgramStatus
from programs.apps.programs.models import Program
from programs.apps.api.serializers import ProgramSerializer


# TODO complete docstring
class ProgramsViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    List / Create Programs.
    """
    queryset = Program.objects.exclude(status=ProgramStatus.DELETED)
    serializer_class = ProgramSerializer
