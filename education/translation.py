"""
Model translations for education app
"""
from modeltranslation.translator import register, TranslationOptions
from .models import EducationCategory, Article, ExamMaterial


@register(EducationCategory)
class EducationCategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


@register(Article)
class ArticleTranslationOptions(TranslationOptions):
    fields = ('title', 'content', 'excerpt', 'author')


@register(ExamMaterial)
class ExamMaterialTranslationOptions(TranslationOptions):
    fields = ('title', 'description')

