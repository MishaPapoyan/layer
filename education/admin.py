from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import EducationCategory, Article, ExamMaterial


@admin.register(EducationCategory)
class EducationCategoryAdmin(TranslationAdmin):
    list_display = ['name', 'icon', 'order', 'is_active']
    list_editable = ['order', 'is_active']


@admin.register(Article)
class ArticleAdmin(TranslationAdmin):
    list_display = ['title', 'category', 'author', 'is_published', 'views', 'created_at']
    list_filter = ['category', 'is_published', 'created_at']
    list_editable = ['is_published']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['views', 'created_at', 'updated_at']


@admin.register(ExamMaterial)
class ExamMaterialAdmin(TranslationAdmin):
    list_display = ['title', 'category', 'order', 'is_active', 'created_at']
    list_filter = ['category', 'is_active']
    list_editable = ['order', 'is_active']

