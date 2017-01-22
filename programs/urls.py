"""programs URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
import os

from auth_backends.urls import auth_urlpatterns
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

from programs.apps.core import views as core_views

admin.autodiscover()

js_info_dict = {
    'packages': ('apps.programs',),
}

urlpatterns = auth_urlpatterns + [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include('programs.apps.api.urls', namespace='api')),
    url(r'^api-auth/', include(auth_urlpatterns, namespace='rest_framework')),
    url(r'^auto_auth/$', core_views.AutoAuth.as_view(), name='auto_auth'),
    url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'^health/$', core_views.health, name='health'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^jsi18n/$', 'django.views.i18n.javascript_catalog', js_info_dict),
]

if settings.DEBUG:  # pragma: no cover
    if os.environ.get('ENABLE_DJANGO_TOOLBAR', False):
        import debug_toolbar  # pylint: disable=import-error,wrong-import-position,wrong-import-order

        urlpatterns.append(
            url(r'^__debug__/', include(debug_toolbar.urls))
        )
