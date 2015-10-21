"""Admin for programs models."""
from django.contrib import admin

from programs.apps.programs import models


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


class ProgramAdmin(admin.ModelAdmin):
    """Admin for the Program model."""
    list_display = ('name', 'status', 'category')
    list_filter = ('status', 'category')
    search_fields = ('name',)
    fields = ('name', 'category', 'status', 'subtitle')
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


class ProgramCourseRunModeAdmin(admin.ModelAdmin):
    """Admin for the ProgramCourseRunMode model."""
    list_display = ('program_course_code', 'course_key')
    search_fields = ('course_key', 'sku')
    fields = ('program_course_code', 'course_key', 'mode_slug', 'sku', 'lms_url')
    raw_id_fields = ('program_course_code',)


admin.site.register(models.Program, ProgramAdmin)
admin.site.register(models.Organization, OrganizationAdmin)
admin.site.register(models.ProgramOrganization, ProgramOrganizationAdmin)
admin.site.register(models.CourseCode, CourseCodeAdmin)
admin.site.register(models.ProgramCourseCode, ProgramCourseCodeAdmin)
admin.site.register(models.ProgramCourseRunMode, ProgramCourseRunModeAdmin)
