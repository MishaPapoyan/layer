"""
Model translations for news app
"""
from modeltranslation.translator import register, TranslationOptions
from .models import NewsCategory, NewsArticle


@register(NewsCategory)
class NewsCategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


@register(NewsArticle)
class NewsArticleTranslationOptions(TranslationOptions):
    fields = ('title', 'content', 'excerpt', 'author')

