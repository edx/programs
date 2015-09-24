# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('name', models.CharField(help_text='The user-facing display name for this Program.', unique=True, max_length=64)),
                ('description', models.TextField(help_text='A full-length description of the Program.', null=True, blank=True)),
                ('category', models.CharField(help_text='The category / type of Program.', max_length=32, choices=[('xseries', 'xseries')])),
                ('certificate_type', models.CharField(blank=True, max_length=32, null=True, help_text='Optional certification criteria for course runs associated with this Program.', choices=[(None, 'None'), ('verified', 'verified')])),
                ('status', models.CharField(default='unpublished', help_text='The lifecycle status of this Program.', max_length=16, choices=[('unpublished', 'unpublished'), ('active', 'active'), ('retired', 'retired'), ('deleted', 'deleted')])),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
    ]
