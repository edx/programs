"""
Image file manipulation functions.

This module was based heavily on
edx-platform/openedx/core/djangoapps/profile_images/images.py, but needed
further generalization to provide correct functionality in this app.
"""
from collections import namedtuple
from cStringIO import StringIO

from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.utils.translation import ugettext as _
from PIL import Image


class ImageValidationError(ValidationError):  # pylint: disable=missing-docstring
    pass


ImageType = namedtuple('ImageType', ('extensions', 'mimetypes', 'file_signatures'))

IMAGE_TYPES = {
    'jpeg': ImageType(
        extensions=['.jpeg', '.jpg'],
        mimetypes=['image/jpeg', 'image/pjpeg'],
        file_signatures=['ffd8'],
    ),
    'png': ImageType(
        extensions=[".png"],
        mimetypes=['image/png'],
        file_signatures=["89504e470d0a1a0a"],
    ),
    'gif': ImageType(
        extensions=[".gif"],
        mimetypes=['image/gif'],
        file_signatures=["474946383961", "474946383761"],
    ),
}


def validate_image_type(uploaded_file):
    """
    Raises ImageValidationError if the server should refuse to use this
    uploaded file based on its apparent type/metadata.  Otherwise, returns
    nothing.

    Arguments:

        uploaded_file (UploadedFile): A user-supplied image file

    Returns:
        None

    Raises:
        ImageValidationError:
            when the image file is an unsupported or invalid type.

    Note:
        Based on original code by @pmitros, adapted from https://github.com/pmitros/ProfileXBlock

    See Also:
        http://en.wikipedia.org/wiki/Magic_number_%28programming%29
        https://en.wikipedia.org/wiki/List_of_file_signatures
    """
    uploaded_file.seek(0)

    # check the file extension looks acceptable
    filename = unicode(uploaded_file.name).lower()
    filetypes = [
        filetype for filetype, imagetype in IMAGE_TYPES.items()
        if any(filename.endswith(ext) for ext in imagetype.extensions)
    ]
    if not filetypes:
        file_upload_bad_type = _(
            u'The file must be one of the following types: {valid_file_types}.'
        ).format(valid_file_types=_get_valid_file_types())
        raise ImageValidationError(file_upload_bad_type)
    image_type = IMAGE_TYPES[filetypes[0]]

    # check mimetype matches expected file type
    if uploaded_file.content_type not in image_type.mimetypes:
        file_upload_bad_mimetype = _(
            u'The Content-Type header for this file does not match '
            u'the file data. The file may be corrupted.'
        )
        raise ImageValidationError(file_upload_bad_mimetype)

    # check file signature matches expected file type
    headers = image_type.file_signatures
    if uploaded_file.read(len(headers[0]) / 2).encode('hex') not in headers:
        file_upload_bad_ext = _(
            u'The file name extension for this file does not match '
            u'the file data. The file may be corrupted.'
        )
        raise ImageValidationError(file_upload_bad_ext)
    # avoid unexpected errors from subsequent modules expecting the fp to be at 0
    uploaded_file.seek(0)


def validate_image_size(uploaded_file, minimum_width, minimum_height):
    """
    Raises ImageValidationError if the uploaded file is not at least as wide
    and tall as the specified dimensions.

    Arguments:
        uploaded_file (UploadedFile): A user-supplied image file
        minimum_width (int): minimum width of the image in pixels
        minimum_height (int): minimum height of the image in pixels

    Returns:
        None

    Raises:
        ImageValidationError:
            when the image file is an unsupported or invalid type.
    """
    image_width, image_height = Image.open(uploaded_file).size
    if image_width < minimum_width or image_height < minimum_height:
        file_upload_too_small = _(
            u'The file must be at least {minimum_width} pixels wide '
            u'and {minimum_height} pixels high.'
        ).format(minimum_width=minimum_width, minimum_height=minimum_height)
        raise ImageValidationError(file_upload_too_small)


def crop_image_to_aspect_ratio(image, aspect_ratio):
    """
    Given a PIL.Image object, return a copy cropped horizontally around the
    center and vertically from the top, using the specified aspect ratio.

    Arguments:
        image (Image): a PIL.Image
        aspect_ratio (float): desired aspect ratio of the cropped image.

    Returns:
        Image
    """
    width, height = image.size
    current_ratio = float(width) / float(height)

    # defaults
    left = 0
    top = 0
    right = width
    bottom = height

    if current_ratio > aspect_ratio:
        # image is too wide and must be cropped horizontally (from center)
        new_width = height * aspect_ratio
        left = (width - new_width) // 2
        right = (width + new_width) // 2
    elif current_ratio < aspect_ratio:
        # image is too tall and must be cropped vertically (from top)
        bottom = width // aspect_ratio
    else:
        # cropping will be a no-op but we'll go ahead, since we promised to
        # return a copy of the input image.
        pass

    image = image.crop(map(int, (left, top, right, bottom)))
    return image


def set_color_mode_to_rgb(image):
    """
    Given a PIL.Image object, return a copy with the color mode set to RGB.

    Arguments:
        image (Image)

    Returns:
        Image
    """
    return image.convert('RGB')


def scale_image(image, width, height):
    """
    Given a PIL.Image object, return a copy resized to the given dimensions.

    Arguments:
        image (Image)
        width (int)
        height (int)

    Returns:
        Image
    """
    return image.resize((width, height), Image.ANTIALIAS)


def create_image_file(image):
    """
    Given a PIL.Image object, create and return a file-like object containing
    the data saved as a JPEG that is compatible with django's storage API.

    Note that the file object returned is a django ContentFile which holds data
    in memory (not on disk).  Because ContentFile does not support a `write`
    call (which is required by PIL.Image.save to serialize itself), we use
    StringIO as an intermediary buffer for the written data, and initialize
    the ContentFile from that.

    Arguments:
        image (Image)

    Returns:
        ContentFile
    """
    string_io = StringIO()
    image.save(string_io, format='JPEG')
    return ContentFile(string_io.getvalue())


def _get_valid_file_types():
    """
    Return comma separated string of valid file types.
    """
    return ', '.join([', '.join(IMAGE_TYPES[ft].extensions) for ft in IMAGE_TYPES])
