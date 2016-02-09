# pylint: disable=missing-docstring
import json
import math

import ddt
from django.conf import settings
from django.core.management import call_command
from django.test import TestCase
import httpretty
import mock

from programs.apps.programs.models import Organization


@ddt.ddt
class SyncOrgsTests(TestCase):
    """Tests for the sync_orgs management command."""
    ORGANIZATIONS_API_URL = settings.ORGANIZATIONS_API_URL_ROOT.strip('/') + '/organizations/'
    RESULT_COUNT = 101
    PAGE_SIZE = settings.ORGANIZATIONS_API_PAGE_SIZE
    PAGE_COUNT = int(math.ceil(RESULT_COUNT / float(PAGE_SIZE)))
    DISPLAY_NAME = 'Organization {} Display Name'
    KEY = 'Organization{}X'

    def _get_body(self, page):
        next_page = page + 1 if page < self.PAGE_COUNT else None
        previous_page = page - 1 if page > 1 else None

        low_id = self.PAGE_SIZE * previous_page + 1 if previous_page else 1
        high_id = self.PAGE_SIZE * page if next_page else self.RESULT_COUNT

        body = {
            'count': self.RESULT_COUNT,
            'next': self.ORGANIZATIONS_API_URL + '?page={}'.format(next_page) if next_page else None,
            'num_pages': self.PAGE_COUNT,
            'previous': self.ORGANIZATIONS_API_URL + '?page={}'.format(previous_page) if previous_page else None,
            'results': [
                {
                    'active': True if i % 2 else False,
                    'created': '2016-02-01T20:09:51.574090Z',
                    'description': 'A great university.',
                    'id': i,
                    'logo': None,
                    'modified': '2016-02-01T20:09:51.575053Z',
                    'name': self.DISPLAY_NAME.format(i),
                    'short_name': self.KEY.format(i)
                }
                for i in range(low_id, high_id + 1)
            ]
        }

        return json.dumps(body)

    def _mock_organizations_api(self):
        self.assertTrue(httpretty.is_enabled(), 'httpretty must be enabled to mock API calls.')

        httpretty.register_uri(
            httpretty.GET,
            self.ORGANIZATIONS_API_URL,
            responses=[
                httpretty.Response(body=self._get_body(page), content_type='application/json')
                for page in range(1, self.PAGE_COUNT + 1)
            ]
        )

    @ddt.data(True, False)
    @httpretty.activate
    def test_handle(self, commit):
        self._mock_organizations_api()
        call_command('sync_orgs', commit=commit)

        # Odd-numbered resources are active.
        expected = math.ceil(self.RESULT_COUNT / 2.0) if commit else 0
        self.assertEqual(Organization.objects.count(), expected)

    @httpretty.activate
    def test_handle_with_existing_records(self):
        for i in range(1, self.RESULT_COUNT + 1):
            Organization.objects.create(
                key=self.KEY.format(i),
                display_name=self.DISPLAY_NAME.format(i)
            )

        self._mock_organizations_api()

        with mock.patch(
            'programs.apps.programs.management.commands.sync_orgs.Organization.objects.create'
        ) as mock_create:
            call_command('sync_orgs', commit=True)

        # Verify that no new orgs were created.
        self.assertEqual(mock_create.called, False)
