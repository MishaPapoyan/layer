from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom User Model with account types"""
    ACCOUNT_TYPES = [
        ('student', 'Student'),
        ('professional', 'Professional'),
        ('lecturer', 'Lecturer'),
    ]
    
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES, default='student')
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True)
    bio = models.TextField(blank=True)
    total_points = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.username} ({self.get_account_type_display()})"


class UserProfile(models.Model):
    """Extended user profile information"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    saved_cases = models.ManyToManyField('cases.LegalCase', blank=True, related_name='saved_by_users')
    saved_articles = models.ManyToManyField('education.Article', blank=True, related_name='saved_by_users')
    
    def __str__(self):
        return f"Profile of {self.user.username}"

