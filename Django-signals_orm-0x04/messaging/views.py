from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages as django_messages
from .models import Message, MessageHistory

@login_required
def edit_message(request, message_id):
    """
    View to edit a message
    """
    message = get_object_or_404(Message, id=message_id, sender=request.user)
    
    if request.method == 'POST':
        old_content = message.content
        new_content = request.POST.get('content')
        
        if new_content and new_content != old_content:
            # Update message - the pre_save signal will handle logging to MessageHistory
            message.content = new_content
            message.edited_by = request.user  # Explicitly set who is editing
            message.save()
            
            django_messages.success(request, "Message updated successfully.")
            return redirect('message_detail', message_id=message.id)
    
    return render(request, 'messaging/edit_message.html', {'message': message})

@login_required
def message_detail(request, message_id):
    """
    View to display message details and edit history
    """
    message = get_object_or_404(Message, id=message_id)
    
    # Check if user has permission to view this message
    if message.sender != request.user and message.receiver != request.user:
        django_messages.error(request, "You don't have permission to view this message.")
        return redirect('inbox')
    
    # Get edit history with optimized query
    edit_history = MessageHistory.objects.filter(message=message).select_related('edited_by').order_by('-edited_at')
    
    context = {
        'message': message,
        'edit_history': edit_history,
    }
    
    return render(request, 'messaging/message_detail.html', context)

@login_required
def inbox_view(request):
    """
    Basic inbox view
    """
    received_messages = Message.objects.filter(receiver=request.user).select_related('sender').order_by('-timestamp')
    sent_messages = Message.objects.filter(sender=request.user).select_related('receiver').order_by('-timestamp')
    
    context = {
        'received_messages': received_messages,
        'sent_messages': sent_messages,
    }
    
    return render(request, 'messaging/inbox.html', context)
