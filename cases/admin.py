from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import LegalCase, CaseAnalysis


@admin.register(LegalCase)
class LegalCaseAdmin(TranslationAdmin):
    list_display = ['title', 'case_type', 'is_active', 'created_by', 'created_at']
    list_filter = ['case_type', 'is_active', 'created_at']
    list_editable = ['is_active']
    search_fields = ['title', 'description', 'scenario']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(CaseAnalysis)
class CaseAnalysisAdmin(admin.ModelAdmin):
    list_display = ['case', 'user', 'is_evaluated', 'score', 'created_at']
    list_filter = ['is_evaluated', 'created_at', 'case__case_type']
    list_editable = ['is_evaluated', 'score']
    search_fields = ['case__title', 'user__username']
    readonly_fields = ['created_at', 'evaluated_at']
    fieldsets = (
        ('Case Information', {'fields': ('case', 'user')}),
        ('Analysis', {'fields': ('hypothesis', 'legal_qualification', 'conclusion')}),
        ('Evaluation', {'fields': ('is_evaluated', 'evaluation', 'score', 'evaluated_at')}),
    )

