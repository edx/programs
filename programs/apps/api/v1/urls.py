""" API v1 URLs. """
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from programs.apps.api.v1 import views


router = DefaultRouter()
router.register(r'programs', views.ProgramsViewSet, base_name='programs')
router.register(r'course_codes', views.CourseCodesViewSet, base_name='course_codes')
router.register(r'organizations', views.OrganizationsViewSet, base_name='organizations')

urlpatterns = [
    url(r'^', include(router.urls)),
]
