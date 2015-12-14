"""
Programs API serializers.

Serializers that can be shared across multiple versions of the API
should be created here. As the API evolves, serializers may become more
specific to a particular version of the API. In this case, the serializers
in question should be moved to versioned sub-package.
"""
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from rest_framework import fields, exceptions, serializers


from programs.apps.programs import models, constants


class NestedWriteableSerializer(serializers.ListSerializer):
    """
    Reusable implementation of updatable nested lists.

    In order to use this serializer class, you must:
      a) specify it as the list_serializer_class for the serializer being nested
      b) define classmethod `unique_attrs(obj)` on the serializer being nested.  That
         method should return a tuple of values that are guaranteed to be unique
         for any child relative to the parent, and it should work with either
         mapping objects (keys) or model instances (attributes).  See the examples
         defined in this file.
    """

    def update(self, instance, validated_data):

        def _key(obj):
            """
            Use unique_attrs to compare across nested json dicts and model
            instances.
            """
            return self.child.unique_attrs(obj)

        db_objs = {_key(obj): obj for obj in instance}
        req_objs = {_key(obj): obj for obj in validated_data}

        # Perform creations and updates.
        ret = []

        for key, req_obj in req_objs.items():
            db_obj = db_objs.get(key)
            if db_obj is None:
                # create the thing
                ret.append(self.child.create(req_obj))
            else:
                # update the thing
                ret.append(self.child.update(db_obj, req_obj))

        # Perform deletions.
        for key, db_obj in db_objs.items():
            if key not in req_objs:
                # delete the thing
                db_obj.delete()

        return ret


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
        list_serializer_class = NestedWriteableSerializer

    @classmethod
    def unique_attrs(cls, obj):
        """
        For use with `NestedWriteableSerializer.update`
        """
        try:
            if isinstance(obj, models.ProgramCourseRunMode):
                return obj.course_key, obj.mode_slug, obj.sku
            else:
                return obj['course_key'], obj['mode_slug'], obj.get('sku')
        except (AttributeError, KeyError) as exc:
            # avoid errors when working with incomplete/invalid nested data
            raise exceptions.ValidationError(exc.message)


class DefaultOrganizationFromContext(object):
    """
    This is here because we need a workaround to prevent ValidationErrors
    in the special case where a CourseCode instance is created on the fly
    while processing nested updates to a Program.  It's based on the
    implementation of `rest_framework.fields.CurrentUserDefault`.  See
    also the inline comments in `ProgramCourseCodeSerializer._get_course_code`.
    """
    def set_context(self, serializer_field):  # pylint: disable=missing-docstring
        self.organization = serializer_field.context['organization']  # pylint: disable=attribute-defined-outside-init

    def __call__(self):  # pylint: disable=missing-docstring
        return self.organization


class CourseCodeSerializer(serializers.ModelSerializer):
    """Serializer for the course code model."""

    class Meta(object):  # pylint: disable=missing-docstring
        model = models.CourseCode
        fields = ('display_name', 'key', 'organization')

    organization = OrganizationSerializer(
        read_only=True,
        default=fields.CreateOnlyDefault(DefaultOrganizationFromContext()),
    )


class ProgramCourseCodeSerializer(serializers.ModelSerializer):
    """Serializer for the program course code model."""

    class Meta(object):  # pylint: disable=missing-docstring
        model = models.ProgramCourseCode
        fields = ('display_name', 'key', 'organization', 'run_modes')
        list_serializer_class = NestedWriteableSerializer

    display_name = serializers.CharField(source='course_code.display_name')
    key = serializers.CharField(source='course_code.key')
    organization = OrganizationSerializer(read_only=True, source='course_code.organization')
    run_modes = ProgramCourseRunModeSerializer(many=True, required=False)

    @classmethod
    def unique_attrs(cls, obj):
        """
        For use with `NestedWriteableSerializer.update`
        """
        if isinstance(obj, models.ProgramCourseCode):
            return obj.course_code.organization.key, obj.course_code.key
        else:
            return obj['course_code'].organization.key, obj['course_code'].key

    def _get_course_code(self, data):
        '''
        Determine the correct CourseCode instance to associate based on
        inbound request data.  This method also handles creating CourseCodes
        on-the-fly when no existing match was found, or updating existing
        instances' display names when they have changed.
        '''
        if 'key' not in data:
            raise ValidationError('Missing course code key.')
        elif 'organization' not in data or 'key' not in data['organization']:
            raise ValidationError('Missing organization information.')

        # find the organization, without which we can't do anything useful.
        try:
            organization = models.Organization.objects.get(key=data[u'organization'][u'key'])
        except models.Organization.DoesNotExist:
            raise ValidationError('Invalid organization key.')
        # extract request data we intend to pass to the serializer
        serializer_data = {k: data[k] for k in ('key', 'display_name') if k in data}
        serializer_data['organization'] = organization

        # try to find an existing course code instance, based on the keys we have.
        try:
            course_code = models.CourseCode.objects.get(key=data[u'key'], organization=organization)
        except models.CourseCode.DoesNotExist:
            course_code = None

        # note that we are passing the organization in the context, because
        # while it's a read-only field on the CourseCodeSerializer, it's needed
        # at create time (and there seems to be no other way to pass it through
        # to the serializer's UniqueTogether validator, which requires its
        # presence).
        #
        # see also: DefaultOrganizationFromContext (in this module)
        # and: http://www.django-rest-framework.org/api-guide/validators/#advanced-default-argument-usage
        cc_serializer = CourseCodeSerializer(
            instance=course_code,
            data=serializer_data,
            partial=True,
            context={'organization': organization},
        )
        cc_serializer.is_valid(raise_exception=True)
        return cc_serializer.save()

    def to_internal_value(self, data):
        """
        Overrides the default deserialization to look up related objects that
        are needed to create/update the correct models.
        """
        out_data = {'program': self.root.instance, 'course_code': self._get_course_code(data)}

        # handle run_modes if present
        if 'run_modes' in data:
            # NB this next block is based on `ModelSerializer.to_internal_value`
            # but has to be duplicated here because the superclass' method is
            # incompatible with nested writes.
            errors = {}
            try:
                validated_value = self.fields['run_modes'].run_validation(data['run_modes'])
            except exceptions.ValidationError as exc:
                errors['run_modes'] = exc.detail
            else:
                fields.set_value(out_data, self.fields['run_modes'].source_attrs, validated_value)

            if errors:
                raise exceptions.ValidationError(errors)

        return out_data

    def _update_run_modes(self, instance, validated_run_modes):
        """
        Call the list serializer associated with the `run_modes` field on this serializer,
        to handle nested list update logic.
        """
        if validated_run_modes is not None:
            for run_mode in validated_run_modes:
                # push down the reference to this parent object before passing data along
                run_mode['program_course_code'] = instance
            try:
                self.fields['run_modes'].update(instance.run_modes.all(), validated_run_modes)
            except ValidationError as exc:
                raise exceptions.ValidationError(list(exc.messages))

    def update(self, instance, validated_data):
        """
        Implement nested writeable run modes during updates.
        """
        run_modes = validated_data.pop('run_modes', None)
        instance = super(ProgramCourseCodeSerializer, self).update(instance, validated_data)
        self._update_run_modes(instance, run_modes)
        return instance

    def create(self, validated_data):
        """
        Implement nested writeable run modes upon creation.
        """
        run_modes = validated_data.pop('run_modes', None)
        instance = super(ProgramCourseCodeSerializer, self).create(validated_data)
        self._update_run_modes(instance, run_modes)
        return instance


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
    course_codes = ProgramCourseCodeSerializer(many=True, source='programcoursecode_set', required=False)

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

    def update(self, instance, validated_data):
        """
        Handle nested data (program course codes) when processing updates.
        """
        program_course_codes = validated_data.pop('programcoursecode_set', None)

        program = super(ProgramSerializer, self).update(instance, validated_data)

        if program_course_codes is not None:
            self.fields['course_codes'].update(instance.programcoursecode_set.all(), program_course_codes)

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
