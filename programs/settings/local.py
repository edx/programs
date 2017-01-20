from programs.settings.base import *

DEBUG = True

# CACHE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
# END CACHE CONFIGURATION

# DATABASE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': root('default.db'),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}
# END DATABASE CONFIGURATION

# EMAIL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# END EMAIL CONFIGURATION

# TOOLBAR CONFIGURATION
# See: http://django-debug-toolbar.readthedocs.org/en/latest/installation.html
if os.environ.get('ENABLE_DJANGO_TOOLBAR', False):
    INSTALLED_APPS += (
        'debug_toolbar',
    )

    MIDDLEWARE_CLASSES += (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )

    DEBUG_TOOLBAR_PATCH_SETTINGS = False

INTERNAL_IPS = ('127.0.0.1',)
# END TOOLBAR CONFIGURATION

# AUTHENTICATION
SOCIAL_AUTH_REDIRECT_IS_HTTPS = False

# Set these to the correct values for your OAuth2/OpenID Connect provider (e.g., devstack)
OAUTH2_PROVIDER_URL = 'http://127.0.0.1:8000/oauth2'
SOCIAL_AUTH_EDX_OIDC_URL_ROOT = OAUTH2_PROVIDER_URL

ENABLE_AUTO_AUTH = True

ORGANIZATIONS_API_URL_ROOT = 'http://127.0.0.1:8000/api/organizations/v0/'

#####################################################################
# Lastly, see if the developer has any local overrides.
if os.path.isfile(join(dirname(abspath(__file__)), 'private.py')):
    from .private import *

# Update JWT_AUTH after private.py, ensuring this section picks up credential overrides.
JWT_AUTH.update({
    'JWT_ISSUERS': [
        {
            'SECRET_KEY': SOCIAL_AUTH_EDX_OIDC_SECRET,
            'ISSUER': OAUTH2_PROVIDER_URL,
            'AUDIENCE': SOCIAL_AUTH_EDX_OIDC_KEY,
        }
    ],
})
