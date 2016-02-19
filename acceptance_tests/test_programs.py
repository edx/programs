# pylint: disable=missing-docstring
from unittest import skipUnless

from bok_choy.web_app_test import WebAppTest

from acceptance_tests.mixins import LogistrationMixin, ProgramManagementMixin
from acceptance_tests.config import ALLOW_DELETE_ALL_PROGRAM, LMS_AUTO_AUTH


class ProgramTests(LogistrationMixin, ProgramManagementMixin, WebAppTest):

    def test_view_programs(self):
        self.login()
        self.assertTrue(self.studio_home_page.view_programs())

    def test_create_program(self):
        self.login()
        self.create_program(
            'testProgram',
            'This is a test program',
            'test_program_marketing_slug')

        # Do program data cleanup
        self.delete_current_program()

    def test_publish_program(self):
        self.login()
        self.create_program(
            'testProgramWithCourse',
            'This is a test program with course',
            'Test_Course_Program')
        try:
            self.manage_program_page.add_course(
                'EDX Demo Course',
                'edx demo')

            self.manage_program_page.add_course_run()
            self.manage_program_page.publish_program()
        finally:
            # We should cleanup the program data regardless if the test suceeded or failed.
            self.delete_current_program()

    @skipUnless(LMS_AUTO_AUTH, 'Without auto auth, we cannot create a non staff user on the fly')
    def test_non_staff_user(self):
        self.login(is_staff=False)
        self.assertFalse(self.studio_home_page.view_programs())

    @skipUnless(ALLOW_DELETE_ALL_PROGRAM, 'Do not run if we should not delete all programs')
    def test_view_no_program(self):
        self.login()
        self.assertTrue(self.delete_all_programs())
        self.assertTrue(self.studio_home_page.is_program_list_empty())
