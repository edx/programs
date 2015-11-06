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


class OrganizationSerializer(serializers.ModelSerializer):
    """Serializer for the organization model."""

    class Meta(object):  # pylint: disable=missing-docstring
        model = models.Organization
        fields = ('display_name', 'key')


class ProgramCourseRunModeSerializer(serializers.ModelSerializer):
    """Serializer for the program course run mode model."""

    class Meta(object):  # pylint: disable=missing-docstring
        model = models.ProgramCourseRunMode
        fields = ('course_key', 'mode_slug', 'sku', 'start_date', 'run_key')


class CourseCodeSerializer(serializers.ModelSerializer):
    """Serializer for the course code model."""

    class Meta(object):  # pylint: disable=missing-docstring
        model = models.CourseCode
        fields = ('display_name', 'key', 'organization')

    organization = OrganizationSerializer(read_only=True)


class ProgramCourseCodeSerializer(serializers.ModelSerializer):
    """Serializer for the program course code model."""

    class Meta(object):  # pylint: disable=missing-docstring
        model = models.ProgramCourseCode
        fields = ('display_name', 'key', 'organization', 'run_modes')

    display_name = serializers.CharField(source='course_code.display_name')
    key = serializers.CharField(source='course_code.key')
    organization = OrganizationSerializer(read_only=True, source='course_code.organization')
    run_modes = ProgramCourseRunModeSerializer(many=True, read_only=True)


class ProgramSerializer(serializers.ModelSerializer):
    """General-purpose serializer for the Program model."""

    class Meta(object):  # pylint: disable=missing-docstring
        model = models.Program
        fields = (
            'id', 'name', 'subtitle', 'category', 'status', 'marketing_slug', 'organizations', 'course_codes',
            'created', 'modified'
        )
        read_only_fields = ('id', 'created', 'modified')

    organizations = OrganizationSerializer(many=True, read_only=True)
    course_codes = ProgramCourseCodeSerializer(many=True, read_only=True, source='programcoursecode_set')

    def validate_status(self, status):
        """
        Prevent creation of Programs with a status other than UNPUBLISHED.
        """
        if self.instance is None and status != constants.ProgramStatus.UNPUBLISHED:
            msg = _("When creating a Program, \"{status}\" is not a valid choice.")
            raise serializers.ValidationError(msg.format(status=status))
        return status
