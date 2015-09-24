# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('programs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='program',
            name='status',
            field=models.CharField(default='unpublished', help_text='The lifecycle status of this Program.', max_length=16, blank=True, choices=[('unpublished', 'unpublished'), ('active', 'active'), ('retired', 'retired'), ('deleted', 'deleted')]),
        ),
    ]
