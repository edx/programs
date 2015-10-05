# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('programs', '0004_remove_program_certificate_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseCode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('key', models.CharField(help_text='The string prefix of opaque keys for runs of this course in the LMS.', max_length=64)),
                ('display_name', models.CharField(help_text='The display name of this course.', max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('key', models.CharField(help_text='The string value of an org key identifying this organization in the LMS.', unique=True, max_length=64, db_index=True)),
                ('display_name', models.CharField(help_text='The display name of this organization.', unique=True, max_length=128)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
        migrations.CreateModel(
            name='ProgramCourseCode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('position', models.IntegerField()),
                ('course_code', models.ForeignKey(to='programs.CourseCode')),
            ],
            options={
                'ordering': ['position'],
            },
        ),
        migrations.CreateModel(
            name='ProgramCourseRunMode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('lms_url', models.CharField(help_text='The URL of the LMS where this course run / mode is being offered.', max_length=1024, null=True)),
                ('course_key', models.CharField(help_text='A string referencing the course key identifying this run / mode in the target LMS.', max_length=256)),
                ('mode_slug', models.CharField(help_text='The mode_slug value which uniquely identifies the mode in the target LMS.', max_length=64)),
                ('sku', models.CharField(help_text='The sku associated with this run/mode in the ecommerce system working with the target LMS.', max_length=255, null=True, blank=True)),
                ('program_course_code', models.ForeignKey(related_name='run_modes', to='programs.ProgramCourseCode')),
            ],
        ),
        migrations.CreateModel(
            name='ProgramOrganization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('organization', models.ForeignKey(to='programs.Organization')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
        migrations.AlterModelOptions(
            name='program',
            options={},
        ),
        migrations.AddField(
            model_name='program',
            name='subtitle',
            field=models.CharField(help_text='A brief, descriptive subtitle for the Program.', max_length=256, null=True, blank=True),
        ),
        migrations.AlterIndexTogether(
            name='program',
            index_together=set([('status', 'category')]),
        ),
        migrations.AddField(
            model_name='programorganization',
            name='program',
            field=models.ForeignKey(to='programs.Program'),
        ),
        migrations.AddField(
            model_name='programcoursecode',
            name='program',
            field=models.ForeignKey(to='programs.Program'),
        ),
        migrations.AddField(
            model_name='organization',
            name='programs',
            field=models.ManyToManyField(related_name='organizations', through='programs.ProgramOrganization', to='programs.Program'),
        ),
        migrations.AddField(
            model_name='coursecode',
            name='organization',
            field=models.ForeignKey(to='programs.Organization'),
        ),
        migrations.AddField(
            model_name='coursecode',
            name='programs',
            field=models.ManyToManyField(related_name='course_codes', through='programs.ProgramCourseCode', to='programs.Program'),
        ),
        migrations.RemoveField(
            model_name='program',
            name='description',
        ),
        migrations.AlterUniqueTogether(
            name='programcourserunmode',
            unique_together=set([('program_course_code', 'course_key', 'mode_slug', 'sku')]),
        ),
        migrations.AlterUniqueTogether(
            name='programcoursecode',
            unique_together=set([('program', 'course_code', 'position')]),
        ),
        migrations.AlterUniqueTogether(
            name='coursecode',
            unique_together=set([('organization', 'key')]),
        ),
    ]
