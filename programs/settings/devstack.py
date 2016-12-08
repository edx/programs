"""Devstack settings"""

from programs.settings.production import *

LOGGING = get_logger_config(debug=True, dev_env=True, local_loglevel='DEBUG')

DEBUG = True
ENABLE_AUTO_AUTH = True

#####################################################################
# Lastly, see if the developer has any local overrides.
if os.path.isfile(join(dirname(abspath(__file__)), 'private.py')):
    from .private import *  # pylint: disable=import-error
