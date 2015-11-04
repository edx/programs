"""
Factories for tests of Programs.
"""
from django.utils.crypto import get_random_string
import factory

from programs.apps.programs import models
from programs.apps.programs.constants import ProgramCategory, ProgramStatus

# pylint: disable=missing-docstring,unnecessary-lambda


class OrganizationFactory(factory.django.DjangoModelFactory):
    class Meta(object):
        model = models.Organization

    id = factory.Sequence(lambda n: n)
    key = factory.LazyAttribute(lambda o: get_random_string(3).upper() + 'x')
    display_name = factory.LazyAttribute(lambda o: '{} Organization'.format(o.key))


class CourseCodeFactory(factory.django.DjangoModelFactory):
    class Meta(object):
        model = models.CourseCode

    id = factory.Sequence(lambda n: n)
    key = factory.LazyAttribute(lambda o: get_random_string(3).upper())
    display_name = factory.LazyAttribute(lambda o: '{} Course'.format(o.key))
    organization = factory.SubFactory(OrganizationFactory)


class ProgramFactory(factory.django.DjangoModelFactory):
    class Meta(object):
        model = models.Program

    name = factory.Sequence(lambda n: 'test-program-{}'.format(n))
    subtitle = "test-subtitle"
    category = ProgramCategory.XSERIES
    status = ProgramStatus.UNPUBLISHED
    marketing_slug = factory.Sequence(lambda n: 'test-slug-{}'.format(n))


class ProgramOrganizationFactory(factory.django.DjangoModelFactory):
    class Meta(object):
        model = models.ProgramOrganization


class ProgramCourseCodeFactory(factory.django.DjangoModelFactory):
    class Meta(object):
        model = models.ProgramCourseCode

    id = factory.Sequence(lambda n: n)


class ProgramCourseRunModeFactory(factory.django.DjangoModelFactory):
    class Meta(object):
        model = models.ProgramCourseRunMode

    id = factory.Sequence(lambda n: n)
    mode_slug = "verified"
    sku = ''
