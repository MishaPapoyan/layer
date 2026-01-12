from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.db import models
from .models import GameType, Game, GameSession, GameQuestion, GameAnswer, Leaderboard, MultiplayerGameRoom
from accounts.models import User


def games_home(request):
    """Games section home"""
    game_types = GameType.objects.filter(is_active=True)
    active_games = Game.objects.filter(is_active=True)[:6]
    
    context = {
        'game_types': game_types,
        'active_games': active_games,
    }
    return render(request, 'games/home.html', context)


def game_type_detail(request, pk):
    """Game type detail page"""
    game_type = get_object_or_404(GameType, pk=pk, is_active=True)
    games = game_type.games.filter(is_active=True)
    
    context = {
        'game_type': game_type,
        'games': games,
    }
    return render(request, 'games/game_type_detail.html', context)


@login_required
def game_detail(request, pk):
    """Game detail and play page"""
    game = get_object_or_404(Game, pk=pk, is_active=True)
    questions = game.questions.all()
    
    # Check if user has an active session
    active_session = GameSession.objects.filter(
        user=request.user,
        game=game,
        completed=False
    ).first()
    
    context = {
        'game': game,
        'questions': questions,
        'active_session': active_session,
    }
    return render(request, 'games/game_detail.html', context)


@login_required
def start_game(request, pk):
    """Start a new game session"""
    game = get_object_or_404(Game, pk=pk, is_active=True)
    
    # Create new session
    session = GameSession.objects.create(
        user=request.user,
        game=game,
        total_points=game.questions.count() * game.points_per_question
    )
    
    return redirect('games:play_game', session_id=session.pk)


@login_required
def play_game(request, session_id):
    """Play game - answer questions"""
    session = get_object_or_404(GameSession, pk=session_id, user=request.user, completed=False)
    questions = session.game.questions.all()
    
    if request.method == 'POST':
        question_id = request.POST.get('question_id')
        answer_id = request.POST.get('answer_id')
        
        question = get_object_or_404(GameQuestion, pk=question_id, game=session.game)
        answer = get_object_or_404(GameAnswer, pk=answer_id, question=question)
        
        # Check if already answered
        submission, created = GameAnswerSubmission.objects.get_or_create(
            session=session,
            question=question,
            defaults={
                'selected_answer': answer,
                'is_correct': answer.is_correct,
                'points_earned': question.points if answer.is_correct else 0,
            }
        )
        
        if not created:
            # Update existing submission
            submission.selected_answer = answer
            submission.is_correct = answer.is_correct
            submission.points_earned = question.points if answer.is_correct else 0
            submission.save()
        
        # Update session score
        session.score = session.submissions.aggregate(
            total=Sum('points_earned')
        )['total'] or 0
        session.save()
        
        # Check if there are more questions
        answered_question_ids = list(session.submissions.values_list('question_id', flat=True))
        remaining_questions = questions.exclude(pk__in=answered_question_ids)
        
        if remaining_questions.exists():
            # Store answer feedback in session for display
            request.session[f'last_answer_{session_id}_{question_id}'] = {
                'correct': answer.is_correct,
                'explanation': answer.explanation,
                'points': submission.points_earned
            }
            messages.success(request, f"Answer submitted! {'Correct! +' + str(submission.points_earned) + ' points' if answer.is_correct else 'Incorrect. Try the next question!'}")
        else:
            # No more questions, complete the game
            from django.utils import timezone
            session.completed = True
            session.completed_at = timezone.now()
            session.save()
            
            # Update user points
            request.user.total_points += session.score
            request.user.save()
            
            # Update leaderboard
            leaderboard, _ = Leaderboard.objects.get_or_create(user=request.user)
            leaderboard.total_points = request.user.total_points
            leaderboard.games_completed = GameSession.objects.filter(
                user=request.user,
                completed=True
            ).count()
            leaderboard.save()
            
            # Update ranks
            update_leaderboard_ranks()
            
            messages.success(request, f"Game completed! You earned {session.score} points!")
            return redirect('games:game_result', session_id=session_id)
        
        return redirect('games:play_game', session_id=session_id)
    
    # Get unanswered questions
    answered_question_ids = session.submissions.values_list('question_id', flat=True)
    current_question = questions.exclude(pk__in=answered_question_ids).first()
    
    if not current_question:
        # All questions answered, complete session
        from django.utils import timezone
        session.completed = True
        session.completed_at = timezone.now()
        session.save()
        
        # Update user points
        request.user.total_points += session.score
        request.user.save()
        
        # Update leaderboard
        leaderboard, _ = Leaderboard.objects.get_or_create(user=request.user)
        leaderboard.total_points = request.user.total_points
        leaderboard.games_completed = GameSession.objects.filter(
            user=request.user,
            completed=True
        ).count()
        leaderboard.save()
        
        # Update ranks
        update_leaderboard_ranks()
        
        messages.success(request, f"Game completed! You earned {session.score} points!")
        return redirect('games:game_result', session_id=session_id)
    
    context = {
        'session': session,
        'current_question': current_question,
        'progress': (len(list(answered_question_ids)) / questions.count()) * 100 if questions.count() > 0 else 0,
    }
    return render(request, 'games/play_game.html', context)


@login_required
def game_result(request, session_id):
    """Game result page"""
    session = get_object_or_404(GameSession, pk=session_id, user=request.user)
    submissions = session.submissions.all().select_related('question', 'selected_answer')
    
    context = {
        'session': session,
        'submissions': submissions,
    }
    return render(request, 'games/game_result.html', context)


def leaderboard(request):
    """Leaderboard page"""
    entries = Leaderboard.objects.all()[:100]
    
    context = {
        'entries': entries,
    }
    return render(request, 'games/leaderboard.html', context)


def update_leaderboard_ranks():
    """Update leaderboard ranks"""
    entries = Leaderboard.objects.all().order_by('-total_points', 'last_updated')
    for rank, entry in enumerate(entries, start=1):
        entry.rank = rank
        entry.save(update_fields=['rank'])


@login_required
def multiplayer_home(request):
    """Multiplayer games home"""
    from .models import MultiplayerGameRoom
    available_rooms = MultiplayerGameRoom.objects.filter(status__in=['waiting', 'ready']).order_by('-created_at')[:10]
    my_rooms = MultiplayerGameRoom.objects.filter(
        Q(created_by=request.user) | Q(player1=request.user) | Q(player2=request.user)
    ).order_by('-created_at')[:5]
    
    context = {
        'available_rooms': available_rooms,
        'my_rooms': my_rooms,
    }
    return render(request, 'games/multiplayer_home.html', context)


@login_required
def create_multiplayer_room(request):
    """Create a new multiplayer game room"""
    from .models import MultiplayerGameRoom
    
    if request.method == 'POST':
        title = request.POST.get('title', 'Courtroom Simulation')
        scenario = request.POST.get('scenario', 'A courtroom simulation where two players compete as legal professionals.')
        
        room = MultiplayerGameRoom.objects.create(
            title=title,
            scenario=scenario,
            created_by=request.user,
            player1=request.user,
            status='waiting'
        )
        
        messages.success(request, f'Room created! Share code: {room.room_code}')
        return redirect('games:multiplayer_room', room_code=room.room_code)
    
    return render(request, 'games/create_multiplayer_room.html')


@login_required
def join_multiplayer_room(request):
    """Join a multiplayer room by code"""
    from .models import MultiplayerGameRoom
    
    if request.method == 'POST':
        room_code = request.POST.get('room_code', '').upper().strip()
        
        try:
            room = MultiplayerGameRoom.objects.get(room_code=room_code)
            
            if room.status in ['waiting', 'ready']:
                if room.player1 == request.user or room.player2 == request.user:
                    messages.info(request, 'You are already in this room!')
                elif not room.player1:
                    room.player1 = request.user
                    room.save()
                elif not room.player2:
                    room.player2 = request.user
                    room.status = 'ready'
                    room.save()
                    messages.success(request, 'Successfully joined room!')
                else:
                    messages.error(request, 'Room is full!')
                return redirect('games:multiplayer_room', room_code=room_code)
            else:
                messages.error(request, 'Room is not available for joining!')
        except MultiplayerGameRoom.DoesNotExist:
            messages.error(request, 'Room not found!')
    
    return redirect('games:multiplayer_home')


@login_required
def multiplayer_room(request, room_code):
    """Multiplayer game room view"""
    from django.utils import timezone
    from .models import MultiplayerGameRoom, MultiplayerGameMove
    
    room = get_object_or_404(MultiplayerGameRoom, room_code=room_code)
    
    # Check if user is part of this room
    if room.created_by != request.user and room.player1 != request.user and room.player2 != request.user:
        messages.error(request, 'You do not have access to this room!')
        return redirect('games:multiplayer_home')
    
    # Start game if both players are ready
    if room.status == 'ready' and room.player1 and room.player2:
        if not room.started_at:
            room.status = 'active'
            room.started_at = timezone.now()
            room.current_turn = room.player1
            room.save()
    
    # Get game moves
    moves = room.moves.all()[:50]
    
    context = {
        'room': room,
        'moves': moves,
        'is_player1': room.player1 == request.user if room.player1 else False,
        'is_player2': room.player2 == request.user if room.player2 else False,
        'is_current_turn': room.current_turn == request.user if room.current_turn else False,
    }
    return render(request, 'games/multiplayer_room.html', context)

