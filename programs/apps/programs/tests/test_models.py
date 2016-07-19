"""
Tests for custom model code in the programs app.
"""
import datetime

import ddt
import pytz
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from programs.apps.programs import models
from programs.apps.programs.constants import ProgramStatus, ProgramCategory
from programs.apps.programs.models import Program, RESIZABLE_IMAGE_SIZES
from programs.apps.programs.tests import factories
from programs.apps.programs.tests.helpers import make_banner_image_file


class TestProgram(TestCase):
    """Tests of the Program model."""
    def test_empty_marketing_slug(self):
        """Verify that multiple Programs can be saved with an empty marketing slug."""
        for i in range(2):
            Program.objects.create(
                name='test-program-{}'.format(i),
                subtitle='test-subtitle',
                category=ProgramCategory.XSERIES,
                status=ProgramStatus.UNPUBLISHED,
                marketing_slug='',
            )

            # Verify that the program was created successfully.
            self.assertEqual(Program.objects.count(), i + 1)

    def test_marketing_slug_uniqueness(self):
        """Verify that multiple Programs can share a non-empty marketing slug."""
        kwargs = {
            'name': 'primary-program',
            'subtitle': 'test-subtitle',
            'category': ProgramCategory.XSERIES,
            'status': ProgramStatus.UNPUBLISHED,
            'marketing_slug': 'test-slug',
        }

        Program.objects.create(**kwargs)

        kwargs['name'] = 'alternate-program',
        Program.objects.create(**kwargs)

        self.assertEqual(len(Program.objects.filter(marketing_slug='test-slug')), 2)

    def test_xseries_activation(self):
        """Verify that an XSeries Program can't be activated with an empty marketing slug."""
        with self.assertRaisesRegexp(
            ValidationError,
            'Active XSeries Programs must have a valid marketing slug.'
        ):
            Program.objects.create(
                name='test-program',
                subtitle='test-subtitle',
                category=ProgramCategory.XSERIES,
                status=ProgramStatus.ACTIVE,
                marketing_slug='',
            )


class TestProgramOrganization(TestCase):
    """
    Tests for the ProgramOrganization model.
    """

    def test_one_org_max(self):
        """
        Ensure that a Program cannot be associated with more than one organization
        (the relationship is modeled as m2m, but initially, we will only allow
        one organization to be associated).
        """
        program = factories.ProgramFactory.create()
        org = factories.OrganizationFactory.create()
        orig_pgm_org = factories.ProgramOrganizationFactory.create(program=program, organization=org)

        # try to add a second association
        org2 = factories.OrganizationFactory.create()
        pgm_org = factories.ProgramOrganizationFactory.build(program=program, organization=org2)
        with self.assertRaises(ValidationError) as context:
            pgm_org.save()
        self.assertEqual('Cannot associate multiple organizations with a program.', context.exception.message)

        # make sure it works to update an existing association
        orig_pgm_org.organization = org2
        orig_pgm_org.save()


class TestProgramCourseCode(TestCase):
    """
    Tests for the ProgramCourseCode model.
    """

    def setUp(self):
        """
        DRY object initializations.
        """
        self.program = factories.ProgramFactory.create()
        self.org = factories.OrganizationFactory.create()
        factories.ProgramOrganizationFactory.create(program=self.program, organization=self.org)
        super(TestProgramCourseCode, self).setUp()

    def test_multi_program_course_association(self):
        """
        Ensure that a CourseCode can be associated with more than one program
        (the relationship is modeled as m2m).
        """

        # Create an initial course code and attach it to a program
        course_code = factories.CourseCodeFactory.create(organization=self.org)
        factories.ProgramCourseCodeFactory.create(program=self.program, course_code=course_code)

        # Ensure that the course code can not be used for different organizations...
        program2 = factories.ProgramFactory.create()
        organization2 = factories.OrganizationFactory.create()
        factories.ProgramOrganizationFactory.create(
            program=program2, organization=organization2
        )
        pgm_course = factories.ProgramCourseCodeFactory.build(program=program2, course_code=course_code)
        with self.assertRaises(ValidationError) as context:
            pgm_course.save()
        self.assertEqual(
            'Course code must be offered by the same organization offering the program.',
            context.exception.message
        )

        # But can be used for multiple programs offered by the same organization
        program3 = factories.ProgramFactory.create()
        factories.ProgramOrganizationFactory.create(program=program3, organization=self.org)
        factories.ProgramCourseCodeFactory.create(program=program3, course_code=course_code)

    def test_position(self):
        """
        Ensure that new ProgramCourseCode rows get automatically assigned an automatically incrementing
        position, and that results are returned by default sorted by ascending position.
        """
        for _ in range(3):
            course_code = factories.CourseCodeFactory.create(organization=self.org)
            factories.ProgramCourseCodeFactory.create(program=self.program, course_code=course_code)

        res = models.ProgramCourseCode.objects.filter(program=self.program)
        self.assertEqual([1, 2, 3], [pgm_course.position for pgm_course in res])

        # shuffle positions.  not worrying about gaps for now.
        res[0].position = 10
        res[0].save()
        # re-fetch, expecting reordering.
        res = models.ProgramCourseCode.objects.filter(program=self.program)
        self.assertEqual([2, 3, 10], [pgm_course.position for pgm_course in res])

    def test_organization(self):
        """
        Ensure that it is not allowed to associate a course code with a program
        when the course code's organization does not match one of the program's
        organizations.
        """
        org2 = factories.OrganizationFactory.create()
        course_code = factories.CourseCodeFactory.create(organization=org2)
        pgm_course = factories.ProgramCourseCodeFactory.build(program=self.program, course_code=course_code)
        with self.assertRaises(ValidationError) as context:
            pgm_course.save()
        self.assertEqual(
            'Course code must be offered by the same organization offering the program.',
            context.exception.message
        )


@ddt.ddt
class TestProgramCourseRunMode(TestCase):
    """
    Tests for the ProgramCourseRunMode model.
    """
    def setUp(self):
        """
        DRY object initializations.
        """
        self.program = factories.ProgramFactory.create()
        self.org = factories.OrganizationFactory.create()
        factories.ProgramOrganizationFactory.create(program=self.program, organization=self.org)
        self.course_code = factories.CourseCodeFactory.create(organization=self.org)
        self.program_course = factories.ProgramCourseCodeFactory.create(
            program=self.program, course_code=self.course_code
        )
        self.start_date = datetime.datetime.now(tz=pytz.UTC)
        self.course_key = 'edX/DemoX/Demo_Course'
        super(TestProgramCourseRunMode, self).setUp()

    def test_duplicate_course_run_mode(self):
        """
        Verify that duplicate course run modes are not allowed for course codes
        in a program.
        """
        kwargs = {
            'program_course_code': self.program_course,
            'course_key': self.course_key,
            'mode_slug': 'test-mode-slug',
            'sku': '',
            'start_date': self.start_date
        }

        factories.ProgramCourseRunModeFactory.create(**kwargs)

        with self.assertRaises(ValidationError) as context:
            factories.ProgramCourseRunModeFactory.create(**kwargs)

        self.assertEqual(
            'Duplicate course run modes are not allowed for course codes in a program.',
            context.exception.message
        )

        kwargs['sku'] = 'test-sku'
        factories.ProgramCourseRunModeFactory.create(**kwargs)

        # Verify that IntegrityErrors aren't raised when someone attempts to create
        # a duplicate course run mode with a non-empty SKU. Previously, the uniqueness
        # constraint across 'program_course_code', 'course_key', 'mode_slug', and 'sku'
        # wasn't manually enforced when a non-empty SKU was provided.
        with self.assertRaises(ValidationError):
            factories.ProgramCourseRunModeFactory.create(**kwargs)

    @ddt.data(
        ('edx/demo/course1', 'course1'),
        ('edx/demo/course2', 'course2'),
        ('course-v1:edX+DemoX+Demo_Course', 'Demo_Course')
    )
    @ddt.unpack
    def test_run_key_parse_from_course_key(self, course_key, run_key):
        """
        Verify that run key is parsed from a given course key and saves into
        the run key.
        """
        prog_course_run_mode = factories.ProgramCourseRunModeFactory.create(
            program_course_code=self.program_course,
            course_key=course_key,
            mode_slug='test-mode-slug',
            sku='',
            start_date=self.start_date
        )
        self.assertEqual(prog_course_run_mode.run_key, run_key)

    @ddt.data('edx/demo', 'course-v1:edX+DemoX', '', 'invalid')
    def test_invalid_course_key(self, course_key):
        """Verify that invalid course key raises error."""
        with self.assertRaises(ValidationError) as context:
            factories.ProgramCourseRunModeFactory.create(
                program_course_code=self.program_course,
                course_key=course_key,
                mode_slug='test-mode-slug',
                sku='',
                start_date=self.start_date
            )

        self.assertEqual(
            'Invalid course key.',
            context.exception.message
        )


class TestProgramDefault(TestCase):
    """
    Test case to validate the ProgramDefault model
    """

    def _create_model_instance(self):
        """
        Helper to create the ProgramDefault model instance
        """
        program_default_instance = factories.ProgramDefaultFactory.create()
        program_default_instance.banner_image = make_banner_image_file('test.jpg')
        program_default_instance.save()
        self.assertEqual(program_default_instance.banner_image.field.sizes, RESIZABLE_IMAGE_SIZES)
        return program_default_instance

    def test_create_first(self):
        """ Verify the first model instance create succeeds """
        self._create_model_instance()

    def test_create_another(self):
        """ Verify validation error if we attempt to create more than 1 ProgramDefault model instance """
        self._create_model_instance()
        with self.assertRaises(IntegrityError):
            factories.ProgramDefaultFactory.create()
