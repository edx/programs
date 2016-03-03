# pylint: disable=missing-docstring
import abc
import json

from bok_choy.page_object import PageObject
from bok_choy.promise import EmptyPromise
from selenium.webdriver.support.select import Select

from acceptance_tests.config import (
    BASIC_AUTH_USERNAME,
    BASIC_AUTH_PASSWORD,
    STUDIO_URL_ROOT,
    PROGRAM_ORGANIZATION,
)


class StudioPage(PageObject):  # pylint: disable=abstract-method
    __metaclass__ = abc.ABCMeta

    def _build_url(self, path):
        url = '{}/{}'.format(STUDIO_URL_ROOT, path)

        if BASIC_AUTH_USERNAME and BASIC_AUTH_PASSWORD:
            url = url.replace('://', '://{}:{}@'.format(BASIC_AUTH_USERNAME, BASIC_AUTH_PASSWORD))

        return url

    def _hide_debug_tool_bar(self):
        if self.q(css='a#djHideToolBarButton').visible:
            # Hide the debug tool bar
            self.q(css='a#djHideToolBarButton').click()

    def _is_browser_on_studio_home(self):
        return self.browser.title.startswith('Studio Home')


class StudioRootPage(StudioPage):
    @property
    def url(self):
        return self._build_url('')

    def is_browser_on_page(self):
        return self.browser.title.startswith('Welcome | Studio')


class StudioLoginPage(StudioPage):
    @property
    def url(self):
        return self._build_url('signin')

    def is_browser_on_page(self):
        return self.q(css='form#login_form').visible

    def login(self, email, password):
        self.q(css='input#email').fill(email)
        self.q(css='input#password').fill(password)
        self.q(css='button.action-primary').click()

        # Wait for LMS to redirect to the dashboard
        EmptyPromise(self._is_browser_on_studio_home, "Studio login redirected to dashboard").fulfill()


class StudioHomePage(StudioPage):
    @property
    def url(self):
        return self._build_url('home')

    def is_browser_on_page(self):
        return self._is_browser_on_studio_home()

    def view_programs(self):
        self.wait_for_element_visibility('ul#course-index-tabs', 'course index tab is now visible')
        # make sure we have access to the programs tab
        if self.q(css='li.programs-tab a').visible:
            # Click on the programs tab and
            self.q(css='li.programs-tab a').click()
            # make sure the programs tab is now visible
            self.wait_for_element_visibility('div.programs-tab', 'programs-tab is visible')
            return True
        else:
            self.wait_for_element_absence(
                'header.has-actions a.new-program-button',
                'new program button is not present')
            return False

    def click_new_program(self):
        # This function would click on the "New Program" button on the header section
        # to go to the new program page on studio.
        self._hide_debug_tool_bar()
        self.wait_for_element_presence('header.has-actions a.new-program-button', 'new program button is present')
        self.q(css='header.has-actions a.new-program-button').click()

    def get_all_program_links(self):
        self.view_programs()
        return self.q(css='a.program-link')

    def is_program_list_empty(self):
        self.view_programs()
        self.wait_for_element_visibility(
            'div.programs-tab a.action-create-program',
            'create new program button in program tab visible')
        return True


class StudioNewProgramPage(StudioPage):
    @property
    def url(self):
        return self._build_url('program/new')

    def is_browser_on_page(self):
        return self.browser.title.startswith('Program Administration') and \
            self.q(css='button.js-create-program').visible

    def create_new_program(self, program_name, program_subtitle, program_marketing_slug):
        self.q(css='input#program-name').fill(program_name)
        self.q(css='input#program-subtitle').fill(program_subtitle)
        self.q(css='input#program-marketing-slug').fill(program_marketing_slug)
        select = Select(self.browser.find_element_by_css_selector('select#program-org'))
        select.select_by_value(PROGRAM_ORGANIZATION)
        # Click on create program button to create the new program
        self.q(css='button.js-create-program').first.click()


class StudioManageProgramPage(StudioPage):
    # Not going to navigate to this page directly
    url = None

    def is_browser_on_page(self):
        return self.q(css='div.js-inline-edit').visible

    def add_course(self, course_code, course_title):
        self.wait_for_element_visibility('button.js-add-course', 'add course button visible')
        self.q(css='button.js-add-course').first.click()
        self.wait_for_element_visibility('input.course-key', 'course code field is visible')
        self.q(css='input.course-key').first.fill(course_code)
        self.q(css='input.display-name').first.fill(course_title)
        self.q(css='button.js-select-course').first.click()

    def add_course_run(self):
        self.wait_for_element_visibility('button.js-add-course-run', 'add course run button visible')
        self.q(css='button.js-add-course-run').first.click()
        self.wait_for_element_visibility(
            'select.js-course-run-select option[value*=\'course\']', 'select course options visible')
        select = Select(self.browser.find_element_by_css_selector('select.js-course-run-select'))
        select.select_by_index(1)

        self.wait_for_element_visibility('button.js-remove-run', 'remove course run button visible')

    def publish_program(self):
        self.wait_for_element_visibility('button.js-publish-program', 'program public button visible')
        self.q(css='button.js-publish-program').first.click()
        self.wait_for_element_visibility('div.confirm-modal button.js-confirm', 'confirmation modal visible')
        self.q(css='div.confirm-modal button.js-confirm').first.click()
        self.wait_for_element_absence('button.js-publish-program', 'publish program button invisible')


class StudioProgramIdTokenPage(StudioPage):
    @property
    def url(self):
        return self._build_url('programs/id_token')

    def is_browser_on_page(self):
        return self.q(css='pre').visible

    def get_token(self):
        token_string = self.q(css='pre').first.text[0]
        token = json.loads(token_string)
        return token['id_token']
