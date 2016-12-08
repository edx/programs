from programs.settings.base import *

# TEST SETTINGS
INSTALLED_APPS += (
    'django_nose',
)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

NOSE_ARGS = [
    '--with-ignore-docstrings',
    '--logging-level=DEBUG',
]

LOGGING['handlers']['local'] = {'class': 'logging.NullHandler'}
# END TEST SETTINGS


# IN-MEMORY TEST DATABASE
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    },
}
# END IN-MEMORY TEST DATABASE

# AUTHENTICATION
OAUTH2_PROVIDER_URL = 'https://test-provider/oauth2'
SOCIAL_AUTH_EDX_OIDC_URL_ROOT = OAUTH2_PROVIDER_URL

JWT_AUTH.update({
    'JWT_ISSUERS': [
        {
            'SECRET_KEY': SOCIAL_AUTH_EDX_OIDC_SECRET,
            'ISSUER': OAUTH2_PROVIDER_URL,
            'AUDIENCE': SOCIAL_AUTH_EDX_OIDC_KEY,
        }
    ],
})
# END AUTHENTICATION

ORGANIZATIONS_API_URL_ROOT = 'http://test-lms.com/api/organizations/v0/'
