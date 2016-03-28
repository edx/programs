"""
Custom S3 storage backends.
"""
from functools import partial

from django.conf import settings
from storages.backends.s3boto import S3BotoStorage


MediaS3BotoStorage = partial(
    S3BotoStorage,
    location=settings.MEDIA_ROOT.strip('/')
)
