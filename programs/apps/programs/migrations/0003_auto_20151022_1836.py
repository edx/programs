# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('programs', '0002_create_groups'),
    ]

    operations = [
        migrations.AlterField(
            model_name='programcourserunmode',
            name='lms_url',
            field=models.CharField(help_text='The URL of the LMS where this course run / mode is being offered.', max_length=1024, null=True, blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='programcoursecode',
            unique_together=set([('program', 'position')]),
        ),
    ]
