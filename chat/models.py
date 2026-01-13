from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class ChatRoom(models.Model):
    """Chat room for consultations"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_rooms')
    lawyer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                              related_name='assigned_chats', limit_choices_to={'account_type': 'professional'})
    subject = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"{self.subject} - {self.user.username}"


class ChatMessage(models.Model):
    """Messages in chat rooms"""
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.sender.username}: {self.message[:50]}"


class ConsultationRequest(models.Model):
    """Scheduled consultation requests"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='consultation_requests')
    lawyer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                              related_name='consultations', limit_choices_to={'account_type': 'professional'})
    subject = models.CharField(max_length=200)
    description = models.TextField()
    preferred_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.subject} - {self.user.username}"


class OnlineChatSession(models.Model):
    """Online chat sessions for widget"""
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='online_chat_sessions')
    session_id = models.CharField(max_length=100, unique=True, help_text='Anonymous session ID for non-authenticated users')
    name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    is_active = models.BooleanField(default=True)
    is_admin_online = models.BooleanField(default=False)
    last_activity = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-last_activity']
    
    def __str__(self):
        if self.user:
            return f"Chat: {self.user.username}"
        return f"Chat: {self.session_id}"


class OnlineChatMessage(models.Model):
    """Messages in online chat widget"""
    session = models.ForeignKey(OnlineChatSession, on_delete=models.CASCADE, related_name='chat_messages')
    sender_type = models.CharField(max_length=20, choices=[('user', 'User'), ('admin', 'Admin')])
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.sender_type}: {self.message[:50]}"


class AdminOnlineStatus(models.Model):
    """Track admin online status"""
    admin = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'is_staff': True})
    is_online = models.BooleanField(default=False)
    last_seen = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = 'Admin Online Status'
    
    def __str__(self):
        return f"{self.admin.username} - {'Online' if self.is_online else 'Offline'}"

