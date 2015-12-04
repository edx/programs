# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('programs', '0004_start_date_run_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='program',
            name='name',
            field=models.CharField(help_text='The user-facing display name for this Program.', unique=True, max_length=255),
        ),
    ]
