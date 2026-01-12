from django.shortcuts import render, get_object_or_404
from .models import EducationCategory, Article, ExamMaterial


def education_home(request):
    """Education section home"""
    categories = EducationCategory.objects.filter(is_active=True)
    context = {
        'categories': categories,
    }
    return render(request, 'education/home.html', context)


def category_detail(request, pk):
    """Category detail with articles"""
    category = get_object_or_404(EducationCategory, pk=pk, is_active=True)
    articles = category.articles.filter(is_published=True)
    exam_materials = category.exam_materials.filter(is_active=True)
    
    context = {
        'category': category,
        'articles': articles,
        'exam_materials': exam_materials,
    }
    return render(request, 'education/category_detail.html', context)


def article_detail(request, slug):
    """Article detail page"""
    article = get_object_or_404(Article, slug=slug, is_published=True)
    article.views += 1
    article.save(update_fields=['views'])
    
    context = {
        'article': article,
    }
    return render(request, 'education/article_detail.html', context)

