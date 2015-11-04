# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import migrations, models
from django.utils.timezone import utc

from opaque_keys import InvalidKeyError
from opaque_keys.edx.keys import CourseKey


def add_run_key(apps, schema_editor):
    """Get the value from course key and parse it through opaque keys.
    Explicitly verifying the format here instead of model save method.
    Otherwise any invalid record in db raises the exception.
    """
    ProgramCourseRunMode = apps.get_model("programs", "ProgramCourseRunMode")
    for course_run_mode in ProgramCourseRunMode.objects.all():
        try:
            course_key = CourseKey.from_string(course_run_mode.course_key)
            course_run_mode.run_key = course_key.run
            course_run_mode.save()
        except InvalidKeyError:
            pass


def remove_run_key(apps, schema_editor):
    """Backward data migration for field 'run_key'."""
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('programs', '0003_program_marketing_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='programcourserunmode',
            name='run_key',
            field=models.CharField(default='', help_text='A string referencing the last part of course key identifying this course run in the target LMS.', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='programcourserunmode',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 5, 7, 39, 2, 791741, tzinfo=utc), help_text='The start date of this course run in the target LMS.'),
            preserve_default=False,
        ),
        migrations.RunPython(add_run_key, remove_run_key),
    ]
