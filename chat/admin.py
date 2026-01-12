from django.contrib import admin
from .models import ChatRoom, ChatMessage, ConsultationRequest


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ['subject', 'user', 'lawyer', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    list_editable = ['is_active']
    search_fields = ['subject', 'user__username']


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['room', 'sender', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    list_editable = ['is_read']
    readonly_fields = ['created_at']
    search_fields = ['message', 'sender__username']


@admin.register(ConsultationRequest)
class ConsultationRequestAdmin(admin.ModelAdmin):
    list_display = ['subject', 'user', 'lawyer', 'status', 'preferred_date', 'created_at']
    list_filter = ['status', 'created_at', 'preferred_date']
    list_editable = ['status']
    search_fields = ['subject', 'user__username']
    readonly_fields = ['created_at']

