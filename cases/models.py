from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class LegalCase(models.Model):
    """Legal cases for case laboratory"""
    CASE_TYPES = [
        ('criminal', 'Criminal Case'),
        ('civil', 'Civil Case'),
        ('administrative', 'Administrative Case'),
    ]
    
    title = models.CharField(max_length=200)
    case_type = models.CharField(max_length=20, choices=CASE_TYPES)
    description = models.TextField()
    scenario = models.TextField(help_text="Case scenario and facts")
    evidence = models.TextField(help_text="Available evidence")
    legal_documents = models.FileField(upload_to='case_documents/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('cases:case_detail', kwargs={'pk': self.pk})


class CaseAnalysis(models.Model):
    """User's analysis of a case"""
    case = models.ForeignKey(LegalCase, on_delete=models.CASCADE, related_name='analyses')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='case_analyses')
    hypothesis = models.TextField(help_text="Investigative hypothesis")
    legal_qualification = models.TextField(help_text="Legal qualification")
    conclusion = models.TextField(help_text="Legal conclusion")
    is_evaluated = models.BooleanField(default=False)
    evaluation = models.TextField(blank=True, help_text="Admin evaluation")
    score = models.IntegerField(default=0, help_text="Score out of 100")
    created_at = models.DateTimeField(auto_now_add=True)
    evaluated_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['case', 'user']
    
    def __str__(self):
        return f"{self.user.username} - {self.case.title}"

