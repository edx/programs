# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('programs', '0003_auto_20150921_1944'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='program',
            name='certificate_type',
        ),
    ]
