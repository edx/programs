"""Tests for Programs fixtures."""
from django.test import TestCase
from django.core.management import call_command


class TestProgramsFixtures(TestCase):
    """Tests preventing Programs fixtures from going stale."""

    def test_sample_data_fixture(self):
        """Attempt installation of the sample data fixture.

        Will fail with an IntegrityError if the Programs schema is altered.
        """
        call_command('loaddata', 'sample_data')
