"""
Model translations for cases app
"""
from modeltranslation.translator import register, TranslationOptions
from .models import LegalCase


@register(LegalCase)
class LegalCaseTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'scenario', 'evidence')

