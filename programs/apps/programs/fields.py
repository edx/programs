"""
Custom fields used in models in the programs django app.
"""
from collections import OrderedDict
from contextlib import closing
import logging
import os
import re

from django.db import models
from django.db.models.fields.files import ImageFieldFile
from PIL import Image

from .image_helpers import (
    create_image_file,
    crop_image_to_aspect_ratio,
    scale_image,
    set_color_mode_to_rgb,
    validate_image_size,
    validate_image_type,
)

LOG = logging.getLogger(__name__)


class ResizingImageFieldFile(ImageFieldFile):
    """
    Custom field value behavior for images stored in `ResizingImageField`
    fields on model instances.  See `ResizingImageField` docs for more info.
    """
    @property
    def resized_names(self):
        """
        Return the names of the resized copies of this image (if any), in a
        dictionary keyed by tuples of (width, height).

        Returns:
            dict
        """
        if not self.name:
            return {}
        else:
            return {
                (width, height): '{}__{}x{}.jpg'.format(self.name, width, height)
                for width, height in self.field.sizes
            }

    @property
    def resized_urls(self):
        """
        Return the URLs of the resized copies of this image (if any), in a
        dictionary keyed by tuples of (width, height).

        Returns:
            dict
        """
        if not self.name:
            return {}
        else:
            return {size: self.storage.url(name) for size, name in self.resized_names.items()}

    @property
    def minimum_original_size(self):
        """
        Return the minimum acceptable width and height of an uploaded image
        (which is the same as the greatest (width, height) pair in
        self.field.sizes).

        Returns:
            tuple(int, int)
        """
        return sorted(self.field.sizes)[-1]

    def create_resized_copies(self):
        """
        Generate and store resized copies of the original image, using the
        django storage API.

        Returns:
            None
        """
        original = Image.open(self.file)
        image = set_color_mode_to_rgb(original)
        ref_width, ref_height = self.minimum_original_size
        image = crop_image_to_aspect_ratio(image, float(ref_width) / float(ref_height))

        for size, name in self.resized_names.items():
            scaled = scale_image(image, *size)
            with closing(create_image_file(scaled)) as scaled_image_file:
                self.storage.save(name, scaled_image_file)

        self.clean_stale_images()

    def clean_stale_images(self, keep_previous=True):
        """
        Search and clean historical images left in the storage,
        using django storage API

        Returns:
            None
        """
        if self.name is None:
            # this method isn't currently used for, and does not support,
            # cleaning up stale copies when the value of the field is currently
            # empty.
            return

        dir_ = self.field.get_path(self.instance)

        groups = {}
        for name in self.storage.listdir(dir_)[1]:
            source_name = re.sub(r'__([\d]+)x([\d]+)\.jpg', '', name)
            groups.setdefault(source_name, []).append(name)

        ordered_groups = OrderedDict(
            sorted(
                groups.items(),
                key=lambda t: self.storage.created_time(os.path.join(dir_, t[0])),
                reverse=True
            )
        )

        current_name = os.path.basename(self.name)
        found_current = found_previous = False
        stale_names = []
        for source_name, group in ordered_groups.items():
            if not found_current:
                found_current = current_name == source_name
            elif keep_previous and not found_previous:
                found_previous = True
            else:
                stale_names += group

        for stale_name in stale_names:
            stale_path = os.path.join(dir_, stale_name)
            LOG.info('Deleting stale image file: %s', stale_path)
            self.storage.delete(stale_path)


class ResizingImageField(models.ImageField):
    """
    Customized ImageField that automatically generates and stores a set of
    resized copies along with the original image files.

    WARNING: this does not presently correct for orientation - processed images
    taken directly from digital cameras may appear with unexpected rotation.

    TODO: purge stale copies.
    """
    attr_class = ResizingImageFieldFile

    def __init__(self, path_template, sizes, *a, **kw):
        """
        Arguments:

            path_template (basestring):
                A format string that will be templated against model
                instances to produce a directory name for stored files.
                For example, if your model has a unique "name" field, you
                could use '/mymodel/{name}/' as the path template.

                To facilitate management/cleanup of stale copies, it's
                important to use a template that will result in a unique and
                immutable value for each model object.

                Note that using the primary key ('id') in your template is
                dangerous, however, because this will evaluate to `None` when
                initially storing a new model instance which has not yet been
                assigned an id by the database.  Therefore, choose a value or
                values which can be assigned before the object is physically
                saved, for example a UUID or an application-generated timestamp.

            sizes:
                A sequence of tuples of (width, height) at which to resize
                copies of the original image.

                The largest of the sizes will be used as the minimum allowed
                dimensions of a newly-stored file.

                WARNING: presently, all of the sizes must have the same aspect
                ratio.
        """
        if callable(kw.get('upload_to')):
            # if an upload_to kwarg is passed with a callable value, the
            # superclass will use it to overwrite the value of
            # self.generate_filename (which is redefined below).
            # Since that will lead to unexpected behavior, prevent it from
            # happening.
            raise Exception(
                'ResizingImageField does not support passing a custom callable '
                'for the `upload_to` keyword arg.'
            )
        super(ResizingImageField, self).__init__(*a, **kw)
        self.path_template = path_template.rstrip('/')
        self.sizes = sizes

    def get_path(self, model_instance):
        """
        Get the calculated path from the path template

        Arguments:

            model_instance (Model):
                The model instance whose value is about to be saved.

        Returns:

            Path (string):
                The path to the file

        """
        return self.path_template.format(**model_instance.__dict__)  # pylint: disable=no-member

    def generate_filename(self, model_instance, filename):  # pylint: disable=method-hidden
        """
        Join our path template with the filename assigned by django storage to
        generate a filename for newly-uploaded file.

        Arguments:

            model_instance (Model):
                The model instance whose value is about to be saved.

            filename (basestring):
                The filename assigned to a newly uploaded file by django.

        Returns:

            ResizingImageFieldFile

        """
        pathname = self.get_path(model_instance)
        return '{}/{}'.format(pathname, filename)

    def pre_save(self, model_instance, add):
        """
        Override pre_save to create resized copies of the original upload
        when necessary (i.e. a newly stored file).

        Arguments:

            model_instance (Model):
                The model instance whose value is about to be saved.

            add (bool):
                Whether the model instance is being added (inserted) for the
                first time.

        Returns:

            ResizingImageFieldFile

        """
        # before invoking super, determine if we are dealing with a file that has previously been saved to storage.
        # we have to check this before calling super since that will store a new file and set _committed to True.
        original_field_value = getattr(model_instance, self.attname)
        originally_committed = getattr(original_field_value, '_committed', False)

        field_value = super(ResizingImageField, self).pre_save(model_instance, add)

        # if we just stored a new file, do additional validation, then generate and save resized copies.
        if not originally_committed:
            validate_image_type(field_value.file)
            validate_image_size(field_value.file, *field_value.minimum_original_size)
            field_value.create_resized_copies()

        return field_value

    def deconstruct(self):
        """
        Provide instantiation metadata for the migrations framework.
        """
        name, path, args, kwargs = super(ResizingImageField, self).deconstruct()
        kwargs['sizes'] = self.sizes
        kwargs['path_template'] = self.path_template
        return name, path, args, kwargs
