# pylint: disable=missing-docstring
import logging
import requests
import uuid

from edx_rest_api_client.client import EdxRestApiClient

from acceptance_tests.config import (
    STUDIO_PASSWORD,
    STUDIO_EMAIL,
    BASIC_AUTH_USERNAME,
    BASIC_AUTH_PASSWORD,
    LMS_URL_ROOT,
    PROGRAMS_URL_ROOT,
    LMS_AUTO_AUTH)
from acceptance_tests.pages import (
    StudioLoginPage,
    StudioHomePage,
    StudioNewProgramPage,
    StudioManageProgramPage,
    StudioProgramIdTokenPage)

log = logging.getLogger(__name__)


class StudioUserMixin(object):
    password = 'edx'

    def generate_user_credentials(self, username_prefix):
        username = username_prefix + uuid.uuid4().hex[0:10]
        password = self.password
        email = '{}@example.com'.format(username)
        return username, email, password

    def create_studio_user(self, is_staff=True):
        username, email, password = self.generate_user_credentials(username_prefix='programs_acceptance')

        url = ('{host}/auto_auth?no_login=true'
               '&username={username}'
               '&password={password}'
               '&email={email}'
               '&staff={staff}').format(host=LMS_URL_ROOT,
                                        username=username,
                                        password=password,
                                        email=email,
                                        staff='true' if is_staff else 'false')

        auth = None

        if BASIC_AUTH_USERNAME and BASIC_AUTH_PASSWORD:
            auth = (BASIC_AUTH_USERNAME, BASIC_AUTH_PASSWORD)

        requests.get(url, auth=auth)

        return username, password, email


class LogistrationMixin(StudioUserMixin):
    def setUp(self):
        super(LogistrationMixin, self).setUp()
        self.studio_login_page = StudioLoginPage(self.browser)

    def login(self, is_staff=True):
        if STUDIO_EMAIL and STUDIO_PASSWORD:
            # If the credential is specified through config, always use the specified credentials
            self.login_with_studio(STUDIO_EMAIL, STUDIO_PASSWORD)
        elif LMS_AUTO_AUTH:
            # Only use auto auth if the config allows it
            _, password, email = self.create_studio_user(is_staff)
            self.login_with_studio(email, password)
        else:
            raise RuntimeError(
                'User credentials have not been provided, and auto auth is not enabled.')

    def login_with_studio(self, email, password):
        # Note: We use Selenium directly here (as opposed to bok-choy) to avoid issues with promises being broken.
        self.studio_login_page.browser.get(self.studio_login_page.url)
        self.studio_login_page.login(email, password)


class ProgramManagementMixin(StudioUserMixin):
    def setUp(self):
        super(ProgramManagementMixin, self).setUp()
        self.session = requests.Session()
        self.studio_home_page = StudioHomePage(self.browser)
        self.manage_program_page = StudioManageProgramPage(self.browser)
        self.program_token_page = StudioProgramIdTokenPage(self.browser)

    def _get_program_jwt_token(self):
        # Get the JWT token from the studio programs id_token page
        self.program_token_page.visit()
        token = self.program_token_page.get_token()
        # Once we get the JWT token, we should go back to the page we
        # came from to maintain the existing state of the test
        self.browser.back()
        return token

    def _get_program_id_from_url(self, url):
        program_id = url.split('/')[-1]
        return program_id

    def _get_current_program_id(self):
        self.assertTrue(self.manage_program_page.is_browser_on_page())
        # Get the newly created program id from the current url
        return self._get_program_id_from_url(self.browser.current_url)

    def create_program(self, name, description, marketing_slug):
        self.studio_home_page.click_new_program()
        new_program_page = StudioNewProgramPage(self.browser)
        new_program_page.wait_for_page()

        # Add the unique program info suffix
        # to make sure we do not have collisions in db
        program_unique_suffix = uuid.uuid4()

        new_program_page.create_new_program(
            '{}_{}'.format(name, program_unique_suffix)[:255],
            '{} {}'.format(description, program_unique_suffix)[:255],
            '{}_{}'.format(marketing_slug, program_unique_suffix)[:255])

        self.manage_program_page.wait_for_page()

    def _delete_program(self, program_id, jwt_token):
        """ With the JWT token, hit the program details URL with the patch to set the
            program status to "deleted". This is the delete program step """

        url = '{0}/api/v1/'.format(PROGRAMS_URL_ROOT)
        delete_client = EdxRestApiClient(url, jwt=jwt_token)
        deleted_program = delete_client.programs(program_id).patch({'status': 'deleted'})
        # tell the caller wither the delete is successful or not.
        return deleted_program['status'] == 'deleted'

    def delete_all_programs(self):
        jwt_token = self._get_program_jwt_token()
        # Make sure we are on the view programs page
        self.assertTrue(self.studio_home_page.is_browser_on_page())
        # Get all the program links from the page, and delete programs one by one
        for program_link in self.studio_home_page.get_all_program_links():
            program_id = self._get_program_id_from_url(program_link.get_attribute('href'))
            if not self._delete_program(program_id, jwt_token):
                log.warning('Set program %s to delete failed using jwt_token %s', program_id, jwt_token)
        return True

    def delete_current_program(self):
        program_id = self._get_current_program_id()
        jwt_token = self._get_program_jwt_token()
        self.assertTrue(self._delete_program(program_id, jwt_token))
