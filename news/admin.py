from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import NewsCategory, NewsArticle


@admin.register(NewsCategory)
class NewsCategoryAdmin(TranslationAdmin):
    list_display = ['name', 'slug', 'order']
    list_editable = ['order']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(NewsArticle)
class NewsArticleAdmin(TranslationAdmin):
    list_display = ['title', 'category', 'author', 'is_published', 'is_featured', 'views', 'created_at']
    list_filter = ['category', 'is_published', 'is_featured', 'created_at']
    list_editable = ['is_published', 'is_featured']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['views', 'created_at', 'updated_at']

