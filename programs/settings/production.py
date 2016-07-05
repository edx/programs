from os import environ
import yaml

from programs.settings.base import *
from programs.settings.utils import get_env_setting, get_logger_config


DEBUG = False
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['*']

# Enable offline compression of CSS/JS
COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True

# Minify CSS
COMPRESS_CSS_FILTERS += [
    'compressor.filters.cssmin.CSSMinFilter',
]

LOGGING = get_logger_config()

# This may be overridden by the yaml in PROGRAMS_CFG, but it should
# be here as a default.
MEDIA_STORAGE_BACKEND = {}

CONFIG_FILE = get_env_setting('PROGRAMS_CFG')
with open(CONFIG_FILE) as f:
    config_from_yaml = yaml.load(f)
    vars().update(config_from_yaml)

    # Load settings for media storage
    vars().update(MEDIA_STORAGE_BACKEND)

DB_OVERRIDES = dict(
    PASSWORD=environ.get('DB_MIGRATION_PASS', DATABASES['default']['PASSWORD']),
    ENGINE=environ.get('DB_MIGRATION_ENGINE', DATABASES['default']['ENGINE']),
    USER=environ.get('DB_MIGRATION_USER', DATABASES['default']['USER']),
    NAME=environ.get('DB_MIGRATION_NAME', DATABASES['default']['NAME']),
    HOST=environ.get('DB_MIGRATION_HOST', DATABASES['default']['HOST']),
    PORT=environ.get('DB_MIGRATION_PORT', DATABASES['default']['PORT']),
)

for override, value in DB_OVERRIDES.iteritems():
    DATABASES['default'][override] = value

JWT_AUTH.update({
    'JWT_ISSUERS': [
        {
            'SECRET_KEY': SOCIAL_AUTH_EDX_OIDC_SECRET,
            'ISSUER': SOCIAL_AUTH_EDX_OIDC_URL_ROOT,
            'AUDIENCE': SOCIAL_AUTH_EDX_OIDC_KEY,
        },
        {
            'SECRET_KEY': LMS_JWT_SECRET_KEY,
            'ISSUER': LMS_JWT_ISSUER,
            'AUDIENCE': LMS_JWT_AUDIENCE,
        },
    ]
})
