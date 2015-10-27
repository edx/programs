# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('programs', '0002_create_groups'),
    ]

    operations = [
        migrations.AddField(
            model_name='program',
            name='marketing_slug',
            field=models.CharField(help_text='Slug used to generate links to the marketing site', max_length=255, unique=True, null=True, blank=True),
        ),
    ]
