""" API v1 URLs. """
from django.conf.urls import url

from programs.apps.api.v1 import views


# TODO can this work properly with a DRF Router?
urlpatterns = [
    url(r'^programs/', views.ProgramsViewSet.as_view({'get': 'list', 'post': 'create'}), name='programs-list'),
]
