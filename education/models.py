from django.db import models
from django.urls import reverse


class EducationCategory(models.Model):
    """Categories for legal education sections"""
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, help_text="Icon class name (e.g., 'fa-gavel', 'fa-book')")
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = 'Education Categories'
        ordering = ['order']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('education:category_detail', kwargs={'pk': self.pk})


class Article(models.Model):
    """Educational articles"""
    category = models.ForeignKey(EducationCategory, on_delete=models.CASCADE, related_name='articles')
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    excerpt = models.TextField(max_length=500, blank=True)
    image = models.ImageField(upload_to='articles/', blank=True, null=True)
    author = models.CharField(max_length=100, blank=True)
    is_published = models.BooleanField(default=True)
    views = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('education:article_detail', kwargs={'slug': self.slug})


class ExamMaterial(models.Model):
    """Exam preparation materials"""
    category = models.ForeignKey(EducationCategory, on_delete=models.CASCADE, related_name='exam_materials')
    title = models.CharField(max_length=200)
    description = models.TextField()
    file = models.FileField(upload_to='exam_materials/', blank=True, null=True)
    link = models.URLField(blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return self.title

