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


class ProgramOrganizationSerializer(serializers.ModelSerializer):
    """Serializer for the organizations for the Program Serializer."""
    display_name = serializers.CharField(source='organization.display_name', read_only=True)
    key = serializers.CharField(source='organization.key')

    class Meta(object):  # pylint: disable=missing-docstring
        model = models.ProgramOrganization
        fields = ('display_name', 'key')
        read_only_fields = ('display_name', )


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

    organizations = ProgramOrganizationSerializer(many=True, source='programorganization_set')
    course_codes = ProgramCourseCodeSerializer(many=True, read_only=True, source='programcoursecode_set')

    def create(self, validated_data):
        """
        Create a Program and link it with the provided organization.
        """
        programs_organizations_data = validated_data.pop('programorganization_set')
        program = super(ProgramSerializer, self).create(validated_data)

        # get organizations with the provided parameter 'key' and attach it
        # with the newly created program
        for organization_data in programs_organizations_data:
            org_data = organization_data.get('organization')
            organization = models.Organization.objects.get(key=org_data.get('key'))
            models.ProgramOrganization.objects.get_or_create(program=program, organization=organization)

        return program

    def validate_status(self, status):
        """
        Prevent creation of Programs with a status other than UNPUBLISHED.
        """
        if self.instance is None and status != constants.ProgramStatus.UNPUBLISHED:
            error_msg = _("When creating a Program, '{status}' is not a valid choice.")
            raise serializers.ValidationError(error_msg.format(status=status))

        return status

    def validate_organizations(self, organizations):
        """
        Prevent creation of Programs without a valid organization.
        """
        error_msg = _("Provide exactly one valid/existing Organization while creating a Program.")

        # validate that user has provided only one organization
        # Note: This is a temporary, application-level constraint for single organization.
        if self.instance is None and len(organizations) != 1:
            raise serializers.ValidationError(error_msg)

        # validate that the provided organization exists in database with
        # the same key
        for organization_data in organizations:
            org_data = organization_data.get('organization')
            if not models.Organization.objects.filter(key=org_data.get('key')).exists():
                error_msg = _("Provided Organization with key '{org_key}' doesn't exist.")
                raise serializers.ValidationError(error_msg.format(org_key=org_data.get('key')))

        return organizations
