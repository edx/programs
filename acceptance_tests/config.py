# pylint: disable=missing-docstring
import os


def str2bool(s):
    s = unicode(s)
    return s.lower() in (u'yes', u'true', u't', u'1')

# TEST CONFIGURATION
ALLOW_DELETE_ALL_PROGRAM = str2bool(os.environ.get('ALLOW_DELETE_ALL_PROGRAM', False))
PROGRAM_ORGANIZATION = os.environ.get('PROGRAM_ORGANIZATION', 'edX')
# END TEST CONFIGURATION

# PROGRAM CONFIGURATION
try:
    PROGRAMS_URL_ROOT = os.environ.get('PROGRAMS_URL_ROOT').strip('/')
except AttributeError:
    raise RuntimeError('A valid url root for the Programs service must be provided to run acceptance tests.')
# END PROGRAM CONFIGURATION

# STUDIO CONFIGURATION
try:
    STUDIO_URL_ROOT = os.environ.get('STUDIO_URL_ROOT').strip('/')
except AttributeError:
    raise RuntimeError('You must provide a valid URL root for Studio to run acceptance tests.')

STUDIO_EMAIL = os.environ.get('STUDIO_EMAIL')
STUDIO_PASSWORD = os.environ.get('STUDIO_PASSWORD')
BASIC_AUTH_USERNAME = os.environ.get('BASIC_AUTH_USERNAME')
BASIC_AUTH_PASSWORD = os.environ.get('BASIC_AUTH_PASSWORD')
# END STUDIO CONFIGURATION

# LMS CONFIGURATION
try:
    LMS_URL_ROOT = os.environ.get('LMS_URL_ROOT').strip('/')
except AttributeError:
    raise RuntimeError('A valid url root for the LMS must be provided to run acceptance tests')

LMS_AUTO_AUTH = str2bool(os.environ.get('LMS_AUTO_AUTH', True))
# END LMS CONFIGURATION
