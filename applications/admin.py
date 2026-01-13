from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import ApplicationType, ApplicationField, ApplicationTemplate, GeneratedApplication


@admin.register(ApplicationType)
class ApplicationTypeAdmin(TranslationAdmin):
    list_display = ['name', 'icon', 'order', 'is_active', 'created_at']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']


@admin.register(ApplicationField)
class ApplicationFieldAdmin(admin.ModelAdmin):
    list_display = ['label', 'application_type', 'field_type', 'is_required', 'order']
    list_filter = ['application_type', 'field_type', 'is_required']
    list_editable = ['order', 'is_required']
    search_fields = ['label', 'field_name', 'application_type__name']
    ordering = ['application_type', 'order']


@admin.register(ApplicationTemplate)
class ApplicationTemplateAdmin(admin.ModelAdmin):
    list_display = ['application_type', 'template_format', 'is_active', 'updated_at']
    list_filter = ['template_format', 'is_active', 'updated_at']
    search_fields = ['application_type__name', 'template_content']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(GeneratedApplication)
class GeneratedApplicationAdmin(admin.ModelAdmin):
    list_display = ['user', 'application_type', 'created_at']
    list_filter = ['application_type', 'created_at']
    search_fields = ['user__username', 'application_type__name']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
