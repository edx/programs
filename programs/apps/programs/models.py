"""
Models for the programs app.
"""
from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.utils.translation import ugettext_lazy as _


from programs.apps.programs import constants


def _choices(*values):
    """
    Helper for use with model field 'choices'.
    """
    return [(value, ) * 2 for value in values]


class Program(TimeStampedModel):
    """
    Representation of a Program.
    """

    name = models.CharField(
        help_text=_('The user-facing display name for this Program.'),
        max_length=64,
        unique=True,
    )

    description = models.TextField(
        help_text=_('A full-length description of the Program.'),
        null=True,
        blank=True,
    )

    category = models.CharField(
        help_text=_('The category / type of Program.'),
        max_length=32,
        choices=_choices(constants.ProgramCategory.XSERIES),
    )

    status = models.CharField(
        help_text=_('The lifecycle status of this Program.'),
        max_length=16,
        choices=_choices(
            constants.ProgramStatus.UNPUBLISHED,
            constants.ProgramStatus.ACTIVE,
            constants.ProgramStatus.RETIRED,
            constants.ProgramStatus.DELETED,
        ),
        default=constants.ProgramStatus.UNPUBLISHED,
        # though this field is not nullable, setting blank=True ensures validators
        # will reject the empty string, instead of implicitly replacing it with the
        # default value.  This is consistent with how None/null is handled.
        blank=True,
    )
