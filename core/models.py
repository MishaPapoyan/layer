from django.db import models
from django.urls import reverse


class SliderItem(models.Model):
    """Home page slider/carousel items"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='slider/')
    button_text = models.CharField(max_length=50, default='Learn More')
    button_link = models.CharField(max_length=200, default='/')
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return self.title


class AboutSection(models.Model):
    """About page content sections"""
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='about/', blank=True, null=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.title


class TeamMember(models.Model):
    """Team members for About page"""
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    bio = models.TextField()
    photo = models.ImageField(upload_to='team/', blank=True, null=True)
    email = models.EmailField(blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.name} - {self.position}"


class ContactInfo(models.Model):
    """Contact information"""
    address = models.TextField()
    phone = models.CharField(max_length=50)
    email = models.EmailField()
    facebook = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    
    class Meta:
        verbose_name_plural = 'Contact Information'
    
    def __str__(self):
        return 'Contact Information'


class ContactMessage(models.Model):
    """Contact form submissions"""
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.subject} - {self.name}"

