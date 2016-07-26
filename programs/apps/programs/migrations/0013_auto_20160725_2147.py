# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('programs', '0012_auto_20160719_1523'),
    ]

    operations = [
        migrations.AlterField(
            model_name='program',
            name='category',
            field=models.CharField(help_text='The category / type of Program.', max_length=32, choices=[('XSeries', 'XSeries'), ('MicroMasters', 'MicroMasters')]),
        ),
    ]
