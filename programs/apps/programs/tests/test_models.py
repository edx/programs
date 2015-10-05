"""
Tests for custom model code in the programs app.
"""
from django.core.exceptions import ValidationError
from django.test import TestCase

from programs.apps.programs import models
from programs.apps.programs.tests import factories


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

    def test_one_program_max(self):
        """
        Ensure that a CourseCode cannot be associated with more than one program
        (the relationship is modeled as m2m, but initially, we will only allow
        one organization to be associated).
        """
        course_code = factories.CourseCodeFactory.create(organization=self.org)
        orig_pgm_course = factories.ProgramCourseCodeFactory.create(program=self.program, course_code=course_code)

        program2 = factories.ProgramFactory.create()
        pgm_course = factories.ProgramCourseCodeFactory.build(program=program2, course_code=course_code)
        with self.assertRaises(ValidationError) as context:
            pgm_course.save()
        self.assertEqual('Cannot associate multiple programs with a course code.', context.exception.message)

        # make sure it works to reassign the existing association to the other program
        orig_pgm_course.program = program2
        orig_pgm_course.save()

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


class TestProgramCourseRunMode(TestCase):
    """
    Tests for the ProgramCourseRunMode model.
    """

    def test_unique_null_sku(self):
        """
        Ensure that ValidationErrors are raised for an attempt to put multiple
        instances of (course_key, mode_slug, sku=NULL) in a program for the
        same course code.
        """
        program = factories.ProgramFactory.create()
        org = factories.OrganizationFactory.create()
        factories.ProgramOrganizationFactory.create(program=program, organization=org)
        course_code = factories.CourseCodeFactory.create(organization=org)
        pgm_course = factories.ProgramCourseCodeFactory.create(program=program, course_code=course_code)

        factories.ProgramCourseRunModeFactory.create(
            program_course_code=pgm_course,
            course_key='test-course-key',
            mode_slug='test-mode-slug',
            sku=None
        )

        with self.assertRaises(ValidationError) as context:
            factories.ProgramCourseRunModeFactory.create(
                program_course_code=pgm_course,
                course_key='test-course-key',
                mode_slug='test-mode-slug',
                sku=None
            )
        self.assertEqual(
            'Duplicate course run modes are not allowed for course codes in a program.',
            context.exception.message
        )

        # this should not cause an error, because the sku has a different non-empty value
        factories.ProgramCourseRunModeFactory.create(
            program_course_code=pgm_course,
            course_key='test-course-key',
            mode_slug='test-mode-slug',
            sku='test-sku'
        )
