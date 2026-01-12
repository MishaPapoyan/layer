from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import (
    GameType, Game, GameQuestion, GameAnswer,
    GameSession, GameAnswerSubmission, Leaderboard,
    MultiplayerGameRoom, MultiplayerGameMove
)


class GameAnswerInline(admin.TabularInline):
    model = GameAnswer
    extra = 2


@admin.register(GameType)
class GameTypeAdmin(TranslationAdmin):
    list_display = ['name', 'game_type', 'order', 'is_active']
    list_editable = ['order', 'is_active']


@admin.register(Game)
class GameAdmin(TranslationAdmin):
    list_display = ['title', 'game_type', 'points_per_question', 'is_active', 'created_at']
    list_filter = ['game_type', 'is_active', 'created_at']
    list_editable = ['is_active']
    search_fields = ['title', 'description', 'scenario']


@admin.register(GameQuestion)
class GameQuestionAdmin(TranslationAdmin):
    list_display = ['question_text', 'game', 'question_type', 'points', 'order']
    list_filter = ['game', 'question_type']
    list_editable = ['order', 'points']
    inlines = [GameAnswerInline]
    search_fields = ['question_text']


@admin.register(GameAnswer)
class GameAnswerAdmin(TranslationAdmin):
    list_display = ['answer_text', 'question', 'is_correct', 'order']
    list_filter = ['is_correct', 'question__game']
    list_editable = ['is_correct', 'order']


@admin.register(GameSession)
class GameSessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'game', 'score', 'total_points', 'completed', 'started_at']
    list_filter = ['completed', 'started_at', 'game']
    readonly_fields = ['started_at', 'completed_at']
    search_fields = ['user__username', 'game__title']


@admin.register(GameAnswerSubmission)
class GameAnswerSubmissionAdmin(admin.ModelAdmin):
    list_display = ['session', 'question', 'is_correct', 'points_earned', 'answered_at']
    list_filter = ['is_correct', 'answered_at']
    readonly_fields = ['answered_at']


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_points', 'games_completed', 'rank', 'last_updated']
    list_editable = ['rank']
    readonly_fields = ['last_updated']
    ordering = ['-total_points']


@admin.register(MultiplayerGameRoom)
class MultiplayerGameRoomAdmin(admin.ModelAdmin):
    list_display = ['room_code', 'title', 'created_by', 'player1', 'player2', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['room_code', 'title', 'created_by__username']
    readonly_fields = ['room_code', 'created_at', 'started_at', 'completed_at']


@admin.register(MultiplayerGameMove)
class MultiplayerGameMoveAdmin(admin.ModelAdmin):
    list_display = ['room', 'player', 'move_type', 'timestamp']
    list_filter = ['move_type', 'timestamp']
    search_fields = ['room__room_code', 'player__username']
    readonly_fields = ['timestamp']

