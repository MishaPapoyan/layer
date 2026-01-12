from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ChatRoom, ChatMessage, ConsultationRequest
from .forms import ConsultationRequestForm


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

