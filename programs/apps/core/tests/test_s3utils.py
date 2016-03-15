"""
Test s3 utilities
"""
from django.test import TestCase
from django.conf import settings
from storages.backends.s3boto import S3BotoStorage

from programs.apps.core.s3utils import MediaS3BotoStorage


class MediaS3BotoStorageTestCase(TestCase):
    """
    Test the MediaS3BotoStorage django storage driver
    """

    def test_storage_init(self):
        """
        The object is just a partial to S3BotoStorage from django-storages,
        with some settings piped in.  Ensure this works as expected.
        """
        storage = MediaS3BotoStorage()
        self.assertIsInstance(storage, S3BotoStorage)
        self.assertEqual(storage.location, settings.MEDIA_ROOT.strip('/'))
