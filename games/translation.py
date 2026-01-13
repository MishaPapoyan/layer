"""
Model translations for games app
"""
from modeltranslation.translator import register, TranslationOptions
from .models import GameType, Game, GameQuestion, GameAnswer, QuizQuestion, QuizAnswer


@register(GameType)
class GameTypeTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


@register(Game)
class GameTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'scenario')


@register(GameQuestion)
class GameQuestionTranslationOptions(TranslationOptions):
    fields = ('question_text',)


@register(GameAnswer)
class GameAnswerTranslationOptions(TranslationOptions):
    fields = ('answer_text', 'explanation')


@register(QuizQuestion)
class QuizQuestionTranslationOptions(TranslationOptions):
    fields = ('question_text',)


@register(QuizAnswer)
class QuizAnswerTranslationOptions(TranslationOptions):
    fields = ('answer_text', 'explanation')

