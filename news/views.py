from django.shortcuts import render, get_object_or_404
from .models import NewsCategory, NewsArticle


def news_home(request):
    """News home page"""
    featured = NewsArticle.objects.filter(is_published=True, is_featured=True)[:3]
    latest = NewsArticle.objects.filter(is_published=True)[:10]
    categories = NewsCategory.objects.all()
    
    context = {
        'featured': featured,
        'latest': latest,
        'categories': categories,
    }
    return render(request, 'news/home.html', context)


def article_detail(request, slug):
    """News article detail"""
    article = get_object_or_404(NewsArticle, slug=slug, is_published=True)
    article.views += 1
    article.save(update_fields=['views'])
    
    # Related articles
    related = NewsArticle.objects.filter(
        category=article.category,
        is_published=True
    ).exclude(pk=article.pk)[:3]
    
    context = {
        'article': article,
        'related': related,
    }
    return render(request, 'news/article_detail.html', context)


def category_detail(request, slug):
    """News category detail"""
    category = get_object_or_404(NewsCategory, slug=slug)
    articles = NewsArticle.objects.filter(category=category, is_published=True)
    
    context = {
        'category': category,
        'articles': articles,
    }
    return render(request, 'news/category_detail.html', context)

