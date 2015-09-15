"""
Factories for tests of Programs.
"""
import factory

from programs.apps.programs.models import Program
from programs.apps.programs.constants import CertificateType, ProgramCategory, ProgramStatus


class ProgramFactory(factory.django.DjangoModelFactory):  # pylint: disable=missing-docstring
    class Meta(object):  # pylint: disable=missing-docstring
        model = Program

    name = factory.Sequence(lambda n: 'test-program-{}'.format(n))  # pylint: disable=unnecessary-lambda
    description = "test-description"
    category = ProgramCategory.XSERIES
    certificate_type = CertificateType.VERIFIED
    status = ProgramStatus.UNPUBLISHED
