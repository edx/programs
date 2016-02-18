"""Tests for program utilities."""
import ddt
from django.test import TestCase

from programs.apps.programs.models import Program, ProgramCourseRunMode
from programs.apps.programs.tests import factories
from programs.apps.programs.utils import ProgramCompletionChecker


PROGRAMS = 3
COURSE_CODES = 3
RUN_MODES = 3


@ddt.ddt
class ProgramCompletionTests(TestCase):
    """Tests for assessing program completion."""
    def setUp(self):
        super(ProgramCompletionTests, self).setUp()

        for i in range(PROGRAMS):
            program = factories.ProgramFactory.create()
            org = factories.OrganizationFactory.create()
            factories.ProgramOrganizationFactory.create(program=program, organization=org)

            for j in range(COURSE_CODES):
                course_code = factories.CourseCodeFactory.create(organization=org)
                program_course_code = factories.ProgramCourseCodeFactory.create(
                    program=program,
                    course_code=course_code
                )

                for k in range(RUN_MODES):
                    factories.ProgramCourseRunModeFactory.create(
                        course_key='org_{}/code_{}/run_{}'.format(i, j, k),
                        program_course_code=program_course_code,
                    )

        self.programs = Program.objects.all()

    @ddt.data(
        (
            [
                # Partially complete program.
                {'course_id': 'org_0/code_0/run_0', 'mode': 'verified'},
            ],
            []
        ),
        (
            [
                # All courses for one program complete, but one invalid run-mode.
                {'course_id': 'org_0/code_0/run_0', 'mode': 'verified'},
                {'course_id': 'org_0/code_1/run_0', 'mode': 'verified'},
                {'course_id': 'org_0/code_2/run_0', 'mode': 'honor'},
            ],
            []
        ),
        (
            [
                # All courses for one program complete with valid run-modes.
                {'course_id': 'org_0/code_0/run_0', 'mode': 'verified'},
                {'course_id': 'org_0/code_1/run_0', 'mode': 'verified'},
                {'course_id': 'org_0/code_2/run_0', 'mode': 'verified'},
            ],
            [1]
        ),
        (
            [
                # All courses for one program complete, across different run-modes.
                {'course_id': 'org_0/code_0/run_0', 'mode': 'verified'},
                {'course_id': 'org_0/code_1/run_1', 'mode': 'verified'},
                {'course_id': 'org_0/code_2/run_2', 'mode': 'verified'},
            ],
            [1]
        ),
        (
            [
                # All courses for two programs complete.
                {'course_id': 'org_0/code_0/run_0', 'mode': 'verified'},
                {'course_id': 'org_0/code_1/run_1', 'mode': 'verified'},
                {'course_id': 'org_0/code_2/run_2', 'mode': 'verified'},
                {'course_id': 'org_2/code_0/run_0', 'mode': 'verified'},
                {'course_id': 'org_2/code_1/run_1', 'mode': 'verified'},
                {'course_id': 'org_2/code_2/run_2', 'mode': 'verified'},
            ],
            [1, 3]
        ),
    )
    @ddt.unpack
    def test_find_completed_programs(self, complete_run_modes, expected_program_ids):
        completion_checker = ProgramCompletionChecker(self.programs, complete_run_modes)
        self.assertEqual(completion_checker.completed_programs, expected_program_ids)

    def test_complete_with_honor_mode(self):
        """
        Explicitly validates that program completion returns a correct result
        for a program with heterogeneous modes across course runs.
        """
        # Update the first run of the first course in the first program,
        # changing it from 'verified' to 'honor'
        run_mode = ProgramCourseRunMode.objects.get(course_key='org_0/code_0/run_0')
        run_mode.mode_slug = 'honor'
        run_mode.save()

        self.assertEqual(
            ProgramCompletionChecker(self.programs, [
                {'course_id': 'org_0/code_0/run_0', 'mode': 'verified'},
                {'course_id': 'org_0/code_1/run_0', 'mode': 'verified'},
                {'course_id': 'org_0/code_2/run_0', 'mode': 'verified'},
            ]).completed_programs,
            []
        )
        self.assertEqual(
            ProgramCompletionChecker(self.programs, [
                {'course_id': 'org_0/code_0/run_0', 'mode': 'honor'},
                {'course_id': 'org_0/code_1/run_0', 'mode': 'verified'},
                {'course_id': 'org_0/code_2/run_0', 'mode': 'verified'},
            ]).completed_programs,
            [1]
        )

    def test_complete_with_mixed_modes(self):
        """
        Explicitly validates that program completion returns a correct result
        for a program with multiple modes for the same course run.
        """
        # Add a second mode for a course run in the first program,
        # so that either the 'verified' or 'honor' mode will count towards
        # completion.
        program_course_code = ProgramCourseRunMode.objects.get(course_key='org_0/code_0/run_0').program_course_code
        factories.ProgramCourseRunModeFactory.create(
            course_key='org_0/code_0/run_0',
            program_course_code=program_course_code,
            mode_slug='honor',
        )

        self.assertEqual(
            ProgramCompletionChecker(self.programs, [
                {'course_id': 'org_0/code_0/run_0', 'mode': 'verified'},
                {'course_id': 'org_0/code_1/run_0', 'mode': 'verified'},
                {'course_id': 'org_0/code_2/run_0', 'mode': 'verified'},
            ]).completed_programs,
            [1]
        )

        self.assertEqual(
            ProgramCompletionChecker(self.programs, [
                {'course_id': 'org_0/code_0/run_0', 'mode': 'honor'},
                {'course_id': 'org_0/code_1/run_0', 'mode': 'verified'},
                {'course_id': 'org_0/code_2/run_0', 'mode': 'verified'},
            ]).completed_programs,
            [1]
        )

    def test_different_modes_in_different_programs(self):
        """
        Explicitly validates that program completion returns a correct result
        when two programs contain different modes of the same course run.
        """
        # Set all of the second program's course runs to match those of the
        # first, and change the mode of one of those runs from 'verified' to
        # 'honor' in the second program.
        for run_mode in ProgramCourseRunMode.objects.filter(program_course_code__program__id=2):
            run_mode.course_key = run_mode.course_key.replace('org_1', 'org_0')
            if run_mode.course_key == 'org_0/code_0/run_0':
                run_mode.mode_slug = 'honor'
            run_mode.save()

        self.assertEqual(
            ProgramCompletionChecker(self.programs, [
                {'course_id': 'org_0/code_0/run_0', 'mode': 'verified'},
                {'course_id': 'org_0/code_1/run_0', 'mode': 'verified'},
                {'course_id': 'org_0/code_2/run_0', 'mode': 'verified'},
            ]).completed_programs,
            [1]
        )

        self.assertEqual(
            ProgramCompletionChecker(self.programs, [
                {'course_id': 'org_0/code_0/run_0', 'mode': 'honor'},
                {'course_id': 'org_0/code_1/run_0', 'mode': 'verified'},
                {'course_id': 'org_0/code_2/run_0', 'mode': 'verified'},
            ]).completed_programs,
            [2]
        )
