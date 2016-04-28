# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import mimetypes
import os
import uuid

from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import migrations, models


def regenerate_uuids(apps, schema_editor):
    """
    If any cases of non-unique uuids are found, regenerate all of the uuids.

    If any images are physically stored in a location referencing an old uuid,
    create a copy and save it with the new uuid.
    """
    Program = apps.get_model('programs', 'Program')

    # first ensure this needs to be done at all.  If no two programs currently
    # have the same uuid value, there's no reason to modify anything.
    # NOTE: if ANY programs have non-unique uuids, ALL programs will have their
    # uuids regenerated.
    counts_by_uuid = Program.objects.values('uuid').annotate(models.Count('id'))
    if not any([r['id__count'] > 1 for r in counts_by_uuid]):
        return

    # give each program a new uuid
    for program in Program.objects.all():
        program.uuid = uuid.uuid4()

        # if a banner image exists, create a new copy stored under the correct uuid.
        old_banner_image = program.banner_image
        if old_banner_image:
            new_image_file = SimpleUploadedFile(
                os.path.basename(old_banner_image.file.name),
                old_banner_image.file.read(),
                mimetypes.guess_type(old_banner_image.file.name)[0]
            )
            program.banner_image = new_image_file

        program.save()


class Migration(migrations.Migration):

    dependencies = [
        ('programs', '0008_auto_20160419_1449'),
    ]

    operations = [
        migrations.RunPython(regenerate_uuids, reverse_code=migrations.RunPython.noop),
        migrations.AlterField(
            model_name='program',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, unique=True, editable=False, blank=True),
        ),
    ]
