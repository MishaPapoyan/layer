from django.contrib import admin
from .models import ChatRoom, ChatMessage, ConsultationRequest, OnlineChatSession, OnlineChatMessage, AdminOnlineStatus


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


@admin.register(OnlineChatSession)
class OnlineChatSessionAdmin(admin.ModelAdmin):
    list_display = ['session_id', 'user', 'name', 'email', 'is_active', 'is_admin_online', 'last_activity', 'created_at']
    list_filter = ['is_active', 'is_admin_online', 'created_at']
    list_editable = ['is_active', 'is_admin_online']
    search_fields = ['session_id', 'name', 'email', 'user__username']
    readonly_fields = ['created_at', 'last_activity']
    list_per_page = 50


@admin.register(OnlineChatMessage)
class OnlineChatMessageAdmin(admin.ModelAdmin):
    list_display = ['session', 'sender_type', 'sender', 'message_preview', 'is_read', 'created_at']
    list_filter = ['sender_type', 'is_read', 'created_at']
    list_editable = ['is_read']
    search_fields = ['message', 'session__session_id', 'session__name']
    readonly_fields = ['created_at']
    
    def message_preview(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    message_preview.short_description = 'Message'


@admin.register(AdminOnlineStatus)
class AdminOnlineStatusAdmin(admin.ModelAdmin):
    list_display = ['admin', 'is_online', 'last_seen']
    list_filter = ['is_online', 'last_seen']
    list_editable = ['is_online']
    search_fields = ['admin__username']

