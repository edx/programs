# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

from programs.apps.core.constants import Role


def create_groups(apps, schema_editor):

    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')
    ContentType = apps.get_model('contenttypes', 'ContentType')

    # these two groups have no permissions for now, but are reserved for future use.
    Group.objects.get_or_create(name=Role.LEARNERS)
    Group.objects.get_or_create(name=Role.AUTHORS)

    admin_group, created = Group.objects.get_or_create(name=Role.ADMINS)
    if created:
        Program = apps.get_model('programs', 'Program')
        content_type = ContentType.objects.get_for_model(Program)

        # This permission would be automatically created by Django with the Program model.  However,
        # during an initial migration, it won't exist yet at the moment this code is executing.
        # Therefore we create the permission manually, in advance, so we can associate it with the
        # new group.
        perm, __ = Permission.objects.get_or_create(codename='add_program', content_type=content_type)
        admin_group.permissions.add(perm)


def destroy_groups(apps, schema_editor):

    Group = apps.get_model('auth', 'Group')
    Group.objects.filter(name__in=(Role.LEARNERS, Role.AUTHORS, Role.ADMINS)).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('programs', '0002_auto_20150921_1925'),
    ]

    operations = [
        migrations.RunPython(create_groups, reverse_code=destroy_groups),
    ]
