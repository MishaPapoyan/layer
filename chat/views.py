from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.utils import timezone
import json
import uuid
from .models import ChatRoom, ChatMessage, ConsultationRequest, OnlineChatSession, OnlineChatMessage, AdminOnlineStatus
from .forms import ConsultationRequestForm


def is_staff(user):
    return user.is_staff


@login_required
def chat_home(request):
    """Chat home - list user's chat rooms"""
    rooms = ChatRoom.objects.filter(user=request.user, is_active=True)
    
    context = {
        'rooms': rooms,
    }
    return render(request, 'chat/home.html', context)


@login_required
def chat_room(request, pk):
    """Chat room detail"""
    room = get_object_or_404(ChatRoom, pk=pk)
    
    # Check access
    if room.user != request.user and room.lawyer != request.user:
        messages.error(request, 'You do not have access to this chat room.')
        return redirect('chat:home')
    
    messages_list = room.messages.all()
    
    # Mark messages as read
    if request.user != room.user:
        messages_list.filter(is_read=False).update(is_read=True)
    
    if request.method == 'POST':
        message_text = request.POST.get('message')
        if message_text:
            ChatMessage.objects.create(
                room=room,
                sender=request.user,
                message=message_text
            )
            return redirect('chat:chat_room', pk=pk)
    
    context = {
        'room': room,
        'messages': messages_list,
    }
    return render(request, 'chat/chat_room.html', context)


@login_required
def create_consultation(request):
    """Create consultation request"""
    if request.method == 'POST':
        form = ConsultationRequestForm(request.POST)
        if form.is_valid():
            consultation = form.save(commit=False)
            consultation.user = request.user
            consultation.save()
            messages.success(request, 'Your consultation request has been submitted!')
            return redirect('chat:consultations')
    else:
        form = ConsultationRequestForm()
    
    context = {
        'form': form,
    }
    return render(request, 'chat/create_consultation.html', context)


@login_required
def consultations(request):
    """List user's consultations"""
    consultations_list = ConsultationRequest.objects.filter(user=request.user)
    
    context = {
        'consultations': consultations_list,
    }
    return render(request, 'chat/consultations.html', context)


# Online Chat Widget Views
def get_or_create_chat_session(request):
    """Get or create chat session for widget"""
    session_id = request.session.get('chat_session_id')
    
    if session_id:
        try:
            session = OnlineChatSession.objects.get(session_id=session_id, is_active=True)
            session.last_activity = timezone.now()
            session.save()
            return session
        except OnlineChatSession.DoesNotExist:
            pass
    
    # Create new session
    session_id = str(uuid.uuid4())
    session = OnlineChatSession.objects.create(
        session_id=session_id,
        user=request.user if request.user.is_authenticated else None,
        name=request.user.get_full_name() if request.user.is_authenticated else '',
        email=request.user.email if request.user.is_authenticated else '',
    )
    request.session['chat_session_id'] = session_id
    return session


@require_http_methods(["GET", "POST"])
@ensure_csrf_cookie
def online_chat_api(request):
    """API endpoint for online chat widget"""
    if request.method == 'GET':
        # Get messages
        session_id = request.session.get('chat_session_id')
        if not session_id:
            return JsonResponse({'messages': [], 'admin_online': False})
        
        try:
            session = OnlineChatSession.objects.get(session_id=session_id)
            messages = OnlineChatMessage.objects.filter(session=session).order_by('created_at')
            messages_data = [{
                'id': msg.id,
                'sender_type': msg.sender_type,
                'message': msg.message,
                'created_at': msg.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            } for msg in messages]
            
            # Check admin online status
            admin_online = AdminOnlineStatus.objects.filter(is_online=True).exists()
            
            return JsonResponse({
                'messages': messages_data,
                'admin_online': admin_online,
                'session_id': session_id
            })
        except OnlineChatSession.DoesNotExist:
            return JsonResponse({'messages': [], 'admin_online': False})
    
    elif request.method == 'POST':
        # Send message
        data = json.loads(request.body)
        message_text = data.get('message', '').strip()
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        
        if not message_text:
            return JsonResponse({'error': 'Message is required'}, status=400)
        
        session = get_or_create_chat_session(request)
        
        # Update session info if provided
        if name:
            session.name = name
        if email:
            session.email = email
        session.save()
        
        # Create message
        sender_type = 'admin' if request.user.is_authenticated and request.user.is_staff else 'user'
        message = OnlineChatMessage.objects.create(
            session=session,
            sender_type=sender_type,
            sender=request.user if request.user.is_authenticated else None,
            message=message_text
        )
        
        return JsonResponse({
            'success': True,
            'message_id': message.id,
            'created_at': message.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })


@login_required
@user_passes_test(is_staff)
def admin_chat_interface(request):
    """Admin interface for managing online chats"""
    
    # Update admin online status
    admin_status, created = AdminOnlineStatus.objects.get_or_create(admin=request.user)
    admin_status.is_online = True
    admin_status.last_seen = timezone.now()
    admin_status.save()
    
    # Get active chat sessions
    active_sessions = OnlineChatSession.objects.filter(is_active=True).order_by('-last_activity')
    
    context = {
        'active_sessions': active_sessions,
    }
    return render(request, 'chat/admin_chat.html', context)


@login_required
@user_passes_test(is_staff)
@require_http_methods(["POST"])
def admin_send_message(request, session_id):
    """Admin sends message to chat session"""
    
    data = json.loads(request.body)
    message_text = data.get('message', '').strip()
    
    if not message_text:
        return JsonResponse({'error': 'Message is required'}, status=400)
    
    try:
        session = OnlineChatSession.objects.get(session_id=session_id)
        message = OnlineChatMessage.objects.create(
            session=session,
            sender_type='admin',
            sender=request.user,
            message=message_text
        )
        
        # Update admin online status
        admin_status, created = AdminOnlineStatus.objects.get_or_create(admin=request.user)
        admin_status.is_online = True
        admin_status.last_seen = timezone.now()
        admin_status.save()
        
        return JsonResponse({
            'success': True,
            'message_id': message.id,
            'created_at': message.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })
    except OnlineChatSession.DoesNotExist:
        return JsonResponse({'error': 'Session not found'}, status=404)


@login_required
@user_passes_test(is_staff)
@require_http_methods(["GET"])
def admin_get_messages(request, session_id):
    """Get messages for a specific session (admin)"""
    
    try:
        session = OnlineChatSession.objects.get(session_id=session_id)
        messages = OnlineChatMessage.objects.filter(session=session).order_by('created_at')
        messages_data = [{
            'id': msg.id,
            'sender_type': msg.sender_type,
            'message': msg.message,
            'created_at': msg.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        } for msg in messages]
        
        return JsonResponse({
            'messages': messages_data,
            'session': {
                'id': session.session_id,
                'name': session.name or 'Anonymous',
                'email': session.email,
                'user': session.user.username if session.user else None,
            }
        })
    except OnlineChatSession.DoesNotExist:
        return JsonResponse({'error': 'Session not found'}, status=404)

