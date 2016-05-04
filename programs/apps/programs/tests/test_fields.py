"""
Tests for custom fields.
"""
import itertools
import random

from django.test import override_settings, TestCase
import ddt
import mock
from PIL import Image

from programs.apps.programs.fields import ResizingImageField, ResizingImageFieldFile
from .helpers import make_image_file, make_uploaded_file

TEST_SIZES = [(1, 1), (999, 999)]
PATCH_MODULE = 'programs.apps.programs.fields'


@override_settings(MEDIA_URL='/test/media/url/')
@ddt.ddt
class ResizingImageFieldFileTestCase(TestCase):
    """
    Test the behavior of values of our custom field in the context of a model
    instance.
    """
    # pylint: disable=too-many-function-args
    # the above is because pylint doesn't seem to understand the method signature of ResizingImageFieldFile.__init__
    # TODO: figure out why this happens

    def setUp(self):
        super(ResizingImageFieldFileTestCase, self).setUp()
        self.model_instance = mock.Mock()
        self.field = ResizingImageField('test-path', TEST_SIZES)

    def test_resized_names(self):
        """
        Ensure the names for resized copies of the image are generated
        correctly.
        """
        field_value = ResizingImageFieldFile(self.model_instance, self.field, 'path/to/test-filename')
        self.assertEqual(
            field_value.resized_names,
            {
                (1, 1): 'path/to/test-filename__1x1.jpg',
                (999, 999): 'path/to/test-filename__999x999.jpg'
            }
        )

    def test_resized_names_no_file(self):
        """
        Ensure the result of generating names is empty when there is no
        original file.
        """
        field_value = ResizingImageFieldFile(self.model_instance, self.field, None)
        self.assertEqual(field_value.resized_names, {})

    def test_resized_urls(self):
        """
        Ensure the URLs for resized copies of the image are generated
        correctly.
        """
        field_value = ResizingImageFieldFile(self.model_instance, self.field, 'path/to/test-filename')
        self.assertEqual(
            field_value.resized_urls,
            {
                (1, 1): '/test/media/url/path/to/test-filename__1x1.jpg',
                (999, 999): '/test/media/url/path/to/test-filename__999x999.jpg'
            }
        )

    def test_resized_urls_no_file(self):
        """
        Ensure the result of generating URLs is empty when there is no
        original file.
        """
        field_value = ResizingImageFieldFile(self.model_instance, self.field, None)
        self.assertEqual(field_value.resized_urls, {})

    def test_minimum_original_size(self):
        """
        Ensure the minimum original size is computed correctly.
        """
        field_value = ResizingImageFieldFile(self.model_instance, self.field, None)
        self.assertEqual(field_value.minimum_original_size, (999, 999))

    def test_create_resized_copies(self):
        """
        Ensure the create_resized_copies function produces and stores copies
        with the correct sizes and data.
        """
        field_value = ResizingImageFieldFile(self.model_instance, self.field, 'test_name')
        with mock.patch.object(field_value, 'storage') as mock_storage:
            with make_image_file((300, 300)) as image_file:
                mock_storage.listdir = mock.Mock(return_value=([], []))
                field_value.file = image_file
                field_value.create_resized_copies()

        self.assertEqual(mock_storage.save.call_count, len(TEST_SIZES))
        actual_calls = dict((v[1] for v in mock_storage.save.mock_calls))
        for width, height in TEST_SIZES:
            expected_name = 'test_name__{}x{}.jpg'.format(width, height)
            actual_data = actual_calls[expected_name]
            image_object = Image.open(actual_data)
            self.assertEqual(image_object.size, (width, height))

    @ddt.data(*itertools.product(
        [['foo', 'bar', 'baz', 'quux'][:n] for n in range(5)],
        [True, False]
    ))
    @ddt.unpack
    def test_clean_stale_images(self, original_names, keep_previous):
        """
        Ensure that previously-stored image files are cleaned up according to our custom logic.
        """
        listdir_results = []
        expected_deleted_names = []
        historical_ctimes = {}
        fake_ctime = 1458446945

        # populate a mock directory (listdir_results) with names of originals and copies
        # and assign incrementing ctimes to the originals
        for i, original_name in enumerate(original_names):
            resized_names = ['{}__{}x{}.jpg'.format(original_name, *size) for size in TEST_SIZES]
            listdir_results += [original_name] + resized_names

            original_path = '{}/{}'.format(self.field.path_template, original_name)
            historical_ctimes[original_path] = fake_ctime
            fake_ctime += 1

            # keep track of the file names we expect to be deleted by this logic
            if i < len(original_names) - (2 if keep_previous else 1):
                expected_deleted_names += [original_name] + resized_names

        random.shuffle(listdir_results)  # ensure names / ctimes are encountered in a random order

        current_name = original_names[-1] if original_names else None
        field_value = ResizingImageFieldFile(self.model_instance, self.field, current_name)

        with mock.patch.object(field_value, 'storage') as mock_storage:
            mock_storage.listdir = mock.Mock(return_value=([], listdir_results))
            mock_storage.delete = mock.Mock(return_value=None)
            mock_storage.created_time = mock.Mock(side_effect=lambda n: historical_ctimes[n])
            field_value.clean_stale_images(keep_previous=keep_previous)

        expected_deleted_paths = ['{}/{}'.format(self.field.path_template, name) for name in expected_deleted_names]
        actual_deleted_paths = [args[0][0] for args in mock_storage.delete.call_args_list]
        self.assertEqual(sorted(expected_deleted_paths), sorted(actual_deleted_paths))


@ddt.ddt
class ResizingImageFieldTestCase(TestCase):
    """
    Test the behavior of the definition of our custom field in the context of a
    model instance.
    """
    def setUp(self):
        super(ResizingImageFieldTestCase, self).setUp()
        self.model_instance = mock.Mock(attr='test-attr')
        self.field = ResizingImageField('testing/{attr}/path', TEST_SIZES)

    def test_generate_filename(self):
        """
        Ensure that the path_template is used to generate filenames correctly.
        """
        self.assertEqual(
            self.field.generate_filename(self.model_instance, 'test-filename'),
            'testing/test-attr/path/test-filename'
        )

    @mock.patch(PATCH_MODULE + '.validate_image_type')
    @mock.patch(PATCH_MODULE + '.validate_image_size')
    @ddt.data(
        (None, False),
        ('test-filename', False),
        ('test-filename', True),
    )
    @ddt.unpack
    def test_pre_save(self, filename, is_existing_file, mock_validate_size, mock_validate_type):
        """
        Ensure that image validation and resizing take place only when a new
        file is being stored.
        """
        # pylint: disable=too-many-function-args

        field_value = ResizingImageFieldFile(self.model_instance, self.field, filename)
        self.model_instance.resized_image = field_value
        self.field.attname = 'resized_image'
        self.field.name = 'resized_image'

        with mock.patch(PATCH_MODULE + '.ResizingImageFieldFile.create_resized_copies') as mock_resize:
            # actual file data is needed for this test to work
            with make_uploaded_file('image/jpeg', (1000, 1000)) as image_file:
                if filename:
                    field_value.file = image_file
                    field_value._committed = is_existing_file  # pylint: disable=protected-access
                self.field.pre_save(self.model_instance, False)

        expected_called = bool(filename) and not is_existing_file
        for actual_called in (mock_validate_size.called, mock_validate_type.called, mock_resize.called):
            self.assertEqual(actual_called, expected_called)

    def test_upload_to(self):
        """
        Ensure that the field cannot be initialized with a callable `upload_to`
        as this will break the filename-generation template logic.
        """
        def dummy_upload_to(instance, filename):  # pylint: disable=missing-docstring, unused-argument
            return 'foo'

        with self.assertRaises(Exception) as exc_context:
            self.field = ResizingImageField('testing/{attr}/path', TEST_SIZES, upload_to=dummy_upload_to)

        self.assertEquals(
            exc_context.exception.message,
            'ResizingImageField does not support passing a custom callable for the `upload_to` keyword arg.',
        )
