# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import programs.apps.programs.fields


class Migration(migrations.Migration):

    dependencies = [
        ('programs', '0009_make_program_uuid_unique'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProgramDefault',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('banner_image', programs.apps.programs.fields.ResizingImageField(sizes=[(1440, 480), (726, 242), (435, 145), (348, 116)], path_template=b'program/banner/default', upload_to=b'', max_length=1000, blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
