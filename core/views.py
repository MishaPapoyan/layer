from django.shortcuts import render, redirect
from django.contrib import messages
from .models import SliderItem, AboutSection, TeamMember, ContactInfo, ContactMessage, BlogPost, Partner, HomeInfoCard, HomeFeature
from .forms import ContactForm


def home(request):
    """Home page with slider"""
    slider_items = SliderItem.objects.filter(is_active=True)
    blog_posts = BlogPost.objects.filter(is_active=True)[:3]
    partners = Partner.objects.filter(is_active=True)
    info_cards = HomeInfoCard.objects.filter(is_active=True)[:4]
    features = HomeFeature.objects.filter(is_active=True)[:6]
    
    # Get latest news
    try:
        from news.models import NewsArticle
        latest_news = NewsArticle.objects.filter(is_published=True)[:3]
    except:
        latest_news = []
    
    # Get active games
    try:
        from games.models import Game
        active_games = Game.objects.filter(is_active=True)[:3]
    except:
        active_games = []
    
    context = {
        'slider_items': slider_items,
        'latest_news': latest_news,
        'active_games': active_games,
        'blog_posts': blog_posts,
        'partners': partners,
        'info_cards': info_cards,
        'features': features,
    }
    return render(request, 'core/home.html', context)


def about(request):
    """About page"""
    sections = AboutSection.objects.filter(is_active=True)
    team_members = TeamMember.objects.filter(is_active=True)
    
    context = {
        'sections': sections,
        'team_members': team_members,
    }
    return render(request, 'core/about.html', context)


def contact(request):
    """Contact page"""
    contact_info = ContactInfo.objects.first()
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')
    else:
        form = ContactForm()
    
    context = {
        'form': form,
        'contact_info': contact_info,
    }
    return render(request, 'core/contact.html', context)

