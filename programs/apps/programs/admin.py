"""Admin for programs models."""
from django import forms
from django.contrib import admin
from opaque_keys import InvalidKeyError
from opaque_keys.edx.keys import CourseKey
from solo.admin import SingletonModelAdmin

from programs.apps.programs import models
from programs.apps.programs.image_helpers import validate_image_type, validate_image_size


class ProgramOrganizationInline(admin.TabularInline):
    """Tabular inline for the ProgramOrganization model."""
    model = models.ProgramOrganization
    raw_id_fields = ('program', 'organization')
    extra = 0


class ProgramCourseCodeInline(admin.TabularInline):
    """Tabular inline for the ProgramCourseCode model."""
    model = models.ProgramCourseCode
    fields = ('program', 'course_code')
    raw_id_fields = ('program', 'course_code')
    extra = 0


class ProgramForm(forms.ModelForm):
    """
    Customizes the django admin form for Programs.
    """

    def clean_banner_image(self):
        """
        Avoid server errors if an uploaded banner image is going to fail validation checks.
        """
        if 'banner_image' in self.files:
            validate_image_type(self.files['banner_image'])
            validate_image_size(self.files['banner_image'], *self.instance.banner_image.minimum_original_size)
        return self.cleaned_data['banner_image']


class ProgramAdmin(admin.ModelAdmin):
    """Admin for the Program model."""
    form = ProgramForm
    list_display = ('name', 'status', 'category')
    list_filter = ('status', 'category')
    search_fields = ('name',)
    fields = ('name', 'category', 'status', 'subtitle', 'marketing_slug', 'banner_image')
    inlines = (ProgramOrganizationInline,)


class OrganizationAdmin(admin.ModelAdmin):
    """Admin for the Organization model."""
    list_display = ('display_name', 'key')
    search_fields = ('display_name', 'key')
    inlines = (ProgramOrganizationInline,)


class ProgramOrganizationAdmin(admin.ModelAdmin):
    """Admin for the m2m ProgramOrganization model."""
    list_display = ('program', 'organization')
    fields = ('program', 'organization')
    raw_id_fields = ('program', 'organization')


class CourseCodeAdmin(admin.ModelAdmin):
    """Admin for the CourseCode model."""
    list_display = ('display_name', 'key', 'organization')
    search_fields = ('display_name', 'key', 'organization__display_name')
    fields = ('key', 'organization', 'display_name')
    raw_id_fields = ('organization',)
    inlines = (ProgramCourseCodeInline,)


class ProgramCourseCodeAdmin(admin.ModelAdmin):
    """Admin for the m2m ProgramCourseCode model."""
    list_display = ('program', 'course_code', 'position')
    search_fields = ('program__name', 'course_code__display_name', 'course_code__key')
    fields = ('program', 'course_code', 'position')
    raw_id_fields = ('program', 'course_code')


class ProgramCourseRunModeForm(forms.ModelForm):
    """Model form for ProgramCourseCode model. Adding custom validation for
    course key format at form level.
    """

    def clean_course_key(self):
        """Clean the course key to make sure format is valid."""
        course_key = self.cleaned_data['course_key']
        try:
            CourseKey.from_string(course_key)
        except InvalidKeyError:
            raise forms.ValidationError('Invalid CourseKey {course_key}!'.format(
                course_key=course_key
            ))

        return course_key

    class Meta(object):  # pylint: disable=missing-docstring
        model = models.ProgramCourseRunMode
        fields = ('program_course_code', 'course_key', 'mode_slug', 'sku', 'lms_url', 'start_date', 'run_key')


class ProgramCourseRunModeAdmin(admin.ModelAdmin):
    """Admin for the ProgramCourseRunMode model."""
    form = ProgramCourseRunModeForm

    list_display = ('program_course_code', 'course_key')
    search_fields = ('course_key', 'sku')
    fields = ('program_course_code', 'course_key', 'mode_slug', 'sku', 'lms_url', 'start_date', 'run_key')
    raw_id_fields = ('program_course_code',)
    readonly_fields = ('run_key',)


admin.site.register(models.Program, ProgramAdmin)
admin.site.register(models.Organization, OrganizationAdmin)
admin.site.register(models.ProgramOrganization, ProgramOrganizationAdmin)
admin.site.register(models.CourseCode, CourseCodeAdmin)
admin.site.register(models.ProgramCourseCode, ProgramCourseCodeAdmin)
admin.site.register(models.ProgramCourseRunMode, ProgramCourseRunModeAdmin)
admin.site.register(models.ProgramDefault, SingletonModelAdmin)
