# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

from django.conf import settings
from programs.apps.core.models import User


def add_service_user(apps, schema_editor):
    """Add service user."""
    user = User.objects.create(username=settings.CREDENTIALS_SERVICE_USERNAME)
    user.set_unusable_password()
    user.save()


def remove_service_user(apps, schema_editor):
    """Remove service user."""
    try:
        User.objects.get(username=settings.CREDENTIALS_SERVICE_USERNAME).delete()
    except User.DoesNotExist:
        return


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_service_user, remove_service_user)
    ]
