from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserProfileForm
from .models import UserProfile
from games.models import GameSession, Leaderboard


def register(request):
    """User registration"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # UserProfile and Leaderboard are created automatically via signals
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('accounts:dashboard')
    else:
        form = UserRegistrationForm()
    
    context = {
        'form': form,
    }
    return render(request, 'accounts/register.html', context)


@login_required
def dashboard(request):
    """User dashboard"""
    user = request.user
    
    # Get user stats
    game_sessions = GameSession.objects.filter(user=user, completed=True)[:5]
    total_games = GameSession.objects.filter(user=user, completed=True).count()
    
    # Get leaderboard position
    leaderboard_entry = Leaderboard.objects.filter(user=user).first()
    rank = leaderboard_entry.rank if leaderboard_entry else None
    
    context = {
        'user': user,
        'game_sessions': game_sessions,
        'total_games': total_games,
        'rank': rank,
    }
    return render(request, 'accounts/dashboard.html', context)


@login_required
def profile(request):
    """User profile page"""
    user = request.user
    profile, _ = UserProfile.objects.get_or_create(user=user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=user)
    
    context = {
        'form': form,
        'profile': profile,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def update_avatar(request):
    """Update user avatar"""
    if request.method == 'POST' and request.FILES.get('profile_image'):
        user = request.user
        user.profile_image = request.FILES['profile_image']
        user.save()
        messages.success(request, 'Avatar updated successfully!')
    return redirect('accounts:dashboard')

