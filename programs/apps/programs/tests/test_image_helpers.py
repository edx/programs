"""
Test cases for image processing helpers.
"""
from contextlib import closing
import os
from tempfile import NamedTemporaryFile

from django.core.files.uploadedfile import UploadedFile
from django.test import TestCase
import ddt
from PIL import Image

from ..image_helpers import (
    ImageValidationError,
    validate_image_type,
    validate_image_size,
    crop_image_to_aspect_ratio,
)
from .helpers import make_image_file, make_uploaded_file


@ddt.ddt
class TestValidateImageType(TestCase):
    """
    Test validate_image_type
    """
    FILE_UPLOAD_BAD_TYPE = (
        u'The file must be one of the following types: .gif, .png, .jpeg, .jpg.'
    )

    def check_validation_result(self, uploaded_file, expected_failure_message):
        """
        Internal DRY helper.
        """
        if expected_failure_message is not None:
            with self.assertRaises(ImageValidationError) as ctx:
                validate_image_type(uploaded_file)
            self.assertEqual(ctx.exception.message, expected_failure_message)
        else:
            validate_image_type(uploaded_file)
            self.assertEqual(uploaded_file.tell(), 0)

    @ddt.data(
        (".gif", "image/gif"),
        (".jpg", "image/jpeg"),
        (".jpeg", "image/jpeg"),
        (".png", "image/png"),
        (".bmp", "image/bmp", FILE_UPLOAD_BAD_TYPE),
        (".tif", "image/tiff", FILE_UPLOAD_BAD_TYPE),
    )
    @ddt.unpack
    def test_extension(self, extension, content_type, expected_failure_message=None):
        """
        Ensure that files whose extension is not supported fail validation.
        """
        with make_uploaded_file(extension=extension, content_type=content_type) as uploaded_file:
            self.check_validation_result(uploaded_file, expected_failure_message)

    def test_extension_mismatch(self):
        """
        Ensure that validation fails when the file extension does not match the
        file data.
        """
        file_upload_bad_ext = (
            u'The file name extension for this file does not match '
            u'the file data. The file may be corrupted.'
        )
        # make a bmp, try to fool the function into thinking it's a jpeg
        with make_image_file(extension=".bmp") as bmp_file:
            with closing(NamedTemporaryFile(suffix=".jpeg")) as fake_jpeg_file:
                fake_jpeg_file.write(bmp_file.read())
                fake_jpeg_file.seek(0)
                uploaded_file = UploadedFile(
                    fake_jpeg_file,
                    content_type="image/jpeg",
                    size=os.path.getsize(fake_jpeg_file.name)
                )
                with self.assertRaises(ImageValidationError) as ctx:
                    validate_image_type(uploaded_file)
                self.assertEqual(ctx.exception.message, file_upload_bad_ext)

    def test_content_type(self):
        """
        Ensure that validation fails when the content_type header and file
        extension do not match
        """
        file_upload_bad_mimetype = (
            u'The Content-Type header for this file does not match '
            u'the file data. The file may be corrupted.'
        )
        with make_uploaded_file(extension=".jpeg", content_type="image/gif") as uploaded_file:
            with self.assertRaises(ImageValidationError) as ctx:
                validate_image_type(uploaded_file)
            self.assertEqual(ctx.exception.message, file_upload_bad_mimetype)


@ddt.ddt
class TestValidateImageSize(TestCase):
    """
    Test validate_image_size
    """

    @ddt.data(
        ((100, 200), (99, 200)),
        ((100, 200), (100, 199)),
        ((2, 2), (1, 2)),
        ((2, 2), (2, 1)),
        ((1000, 1000), (1, 1)),
    )
    @ddt.unpack
    def test_validate_image_size_invalid(self, required_dimensions, actual_dimensions):

        expected_message = u'The file must be at least {} pixels wide and {} pixels high.'.format(*required_dimensions)

        with make_uploaded_file("image/jpeg", actual_dimensions) as uploaded_file:
            with self.assertRaises(ImageValidationError) as ctx:
                validate_image_size(uploaded_file, *required_dimensions)
            self.assertEqual(ctx.exception.message, expected_message)

    @ddt.data(
        ((100, 200), (100, 200)),
        ((100, 200), (101, 201)),
        ((1, 1), (1, 1)),
        ((100, 100), (1000, 1000)),
    )
    @ddt.unpack
    def test_validate_image_size_valid(self, required_dimensions, actual_dimensions):

        with make_uploaded_file("image/jpeg", actual_dimensions) as uploaded_file:
            self.assertIsNone(validate_image_size(uploaded_file, *required_dimensions))


class TestCropImageToAspectRatio(TestCase):
    """
    Test crop_image_to_aspect_ratio

    TODO: this does not test where images are being cropped from, just that the
    sizing math is correct.
    """

    def test_crop_image(self):
        """
        Ensure the resulting cropped Image has the correct dimensions.
        """
        with make_image_file((300, 200)) as image_file:
            with closing(Image.open(image_file)) as image_obj:

                # reduce lesser dimension (height) to achieve 2:1
                cropped = crop_image_to_aspect_ratio(image_obj, 2)
                self.assertEqual(cropped.size, (300, 150))

                # reduce greater dimension (width) to achieve 0.5:1
                cropped = crop_image_to_aspect_ratio(image_obj, 0.5)
                self.assertEqual(cropped.size, (100, 200))

                # reduce greater dimension (width) to achieve 1:1
                cropped = crop_image_to_aspect_ratio(image_obj, 1)
                self.assertEqual(cropped.size, (200, 200))

                # no cropping necessary, aspect ratio already correct
                cropped = crop_image_to_aspect_ratio(image_obj, 1.5)
                self.assertEqual(cropped.size, (300, 200))
