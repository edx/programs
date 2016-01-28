"""Tests for program utilities."""
import ddt
from django.test import TestCase

from programs.apps.programs.models import Program
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
