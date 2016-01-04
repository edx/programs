# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('programs', '0005_auto_20151204_2212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='program',
            name='marketing_slug',
            field=models.CharField(default='', help_text='Slug used to generate links to the marketing site', max_length=255, blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='program',
            name='subtitle',
            field=models.CharField(default='', help_text='A brief, descriptive subtitle for the Program.', max_length=255, blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='programcourserunmode',
            name='lms_url',
            field=models.CharField(default='', help_text='The URL of the LMS where this course run / mode is being offered.', max_length=1024, blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='programcourserunmode',
            name='sku',
            field=models.CharField(default='', help_text='The sku associated with this run/mode in the ecommerce system working with the target LMS.', max_length=255, blank=True),
            preserve_default=False,
        ),
    ]
