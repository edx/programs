# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('programs', '0010_programdefault'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='display_name',
            field=models.CharField(help_text='The display name of this organization.', max_length=128),
        ),
    ]
