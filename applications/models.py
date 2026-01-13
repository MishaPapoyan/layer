from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class ApplicationType(models.Model):
    """Types of legal applications (Statement of Claim, Court Application, etc.)"""
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default='📄', help_text='Emoji or icon code')
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Application Type'
        verbose_name_plural = 'Application Types'
    
    def __str__(self):
        return self.name


class ApplicationField(models.Model):
    """Dynamic input fields for application types"""
    FIELD_TYPES = [
        ('text', 'Text Input'),
        ('textarea', 'Text Area'),
        ('email', 'Email'),
        ('date', 'Date'),
        ('number', 'Number'),
        ('select', 'Dropdown'),
        ('checkbox', 'Checkbox'),
    ]
    
    application_type = models.ForeignKey(ApplicationType, on_delete=models.CASCADE, related_name='fields')
    field_name = models.CharField(max_length=100, help_text='Internal field name (e.g., full_name)')
    label = models.CharField(max_length=200, help_text='Display label (e.g., Full Name)')
    field_type = models.CharField(max_length=20, choices=FIELD_TYPES, default='text')
    placeholder = models.CharField(max_length=200, blank=True)
    help_text = models.TextField(blank=True, help_text='Help text shown below the field')
    is_required = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    options = models.TextField(blank=True, help_text='For select/checkbox: comma-separated options')
    validation_regex = models.CharField(max_length=200, blank=True, help_text='Optional regex pattern for validation')
    
    class Meta:
        ordering = ['order', 'field_name']
    
    def __str__(self):
        return f"{self.application_type.name} - {self.label}"


class ApplicationTemplate(models.Model):
    """Document templates for application types"""
    application_type = models.OneToOneField(ApplicationType, on_delete=models.CASCADE, related_name='template')
    template_content = models.TextField(help_text='Template with placeholders like {{field_name}}')
    template_format = models.CharField(max_length=10, choices=[('pdf', 'PDF'), ('docx', 'DOCX')], default='pdf')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Application Template'
        verbose_name_plural = 'Application Templates'
    
    def __str__(self):
        return f"Template for {self.application_type.name}"


class GeneratedApplication(models.Model):
    """Generated applications by users"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='generated_applications')
    application_type = models.ForeignKey(ApplicationType, on_delete=models.CASCADE)
    field_data = models.JSONField(help_text='Stored form data as JSON')
    generated_file = models.FileField(upload_to='applications/generated/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.application_type.name} - {self.created_at.date()}"
