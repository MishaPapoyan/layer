"""
Model translations for applications app
"""
from modeltranslation.translator import register, TranslationOptions
from .models import ApplicationType


@register(ApplicationType)
class ApplicationTypeTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


