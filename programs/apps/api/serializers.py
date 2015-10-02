"""
Programs API serializers.

Serializers that can be shared across multiple versions of the API
should be created here. As the API evolves, serializers may become more
specific to a particular version of the API. In this case, the serializers
in question should be moved to versioned sub-package.
"""
from django.utils.translation import ugettext as _
from rest_framework import serializers


from programs.apps.programs import models, constants


class ProgramSerializer(serializers.ModelSerializer):
    """General-purpose serializer for the Program model."""

    class Meta(object):  # pylint: disable=missing-docstring
        model = models.Program
        fields = ('id', 'name', 'description', 'category', 'status', 'created', 'modified')
        read_only_fields = ('id', 'created', 'modified')

    def validate_status(self, status):
        """
        Prevent creation of Programs with a status other than UNPUBLISHED.
        """
        if self.instance is None and status != constants.ProgramStatus.UNPUBLISHED:
            msg = _("When creating a Program, \"{status}\" is not a valid choice.")
            raise serializers.ValidationError(msg.format(status=status))
        return status
