# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import programs.apps.programs.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('programs', '0006_auto_20160104_1920'),
    ]

    operations = [
        migrations.AddField(
            model_name='program',
            name='banner_image',
            field=programs.apps.programs.fields.ResizingImageField(path_template=b'program/banner/{uuid}', null=True, upload_to=b'', sizes=[(1440, 480), (480, 160), (360, 120), (180, 60)], blank=True),
        ),
        migrations.AddField(
            model_name='program',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, blank=True),
        ),
    ]
