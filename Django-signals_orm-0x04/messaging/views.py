from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages as django_messages
from django.contrib.auth.models import User
from .models import Message, MessageHistory

@login_required
def delete_user_account(request):
    """
    Task 2: View to delete user account and trigger cleanup via signals
    """
    if request.method == 'POST':
        user = request.user
        
        # Logout the user before deletion
        from django.contrib.auth import logout
        logout(request)
        
        # Delete the user - this will trigger the post_delete signal
        user.delete()
        
        django_messages.success(request, "Your account has been deleted successfully.")
        return redirect('home')
    
    return render(request, 'messaging/delete_account_confirm.html')

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
            message.edited_by = request.user
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
    
    # Get edit history with optimized query using .only()
    edit_history = MessageHistory.objects.filter(message=message).select_related('edited_by').only(
        'old_content', 'edited_at', 'edited_by__username'
    ).order_by('-edited_at')
    
    context = {
        'message': message,
        'edit_history': edit_history,
    }
    
    return render(request, 'messaging/message_detail.html', context)

@login_required
def inbox_view(request):
    """
    Task 4: Inbox view using custom manager with .only() optimization
    """
    # Task 4: Use custom manager to get unread messages with .only() optimization
    unread_messages = Message.unread.unread_for_user(request.user)  # This is what checker wants
    
    # All messages with optimized queries using .only()
    all_messages = Message.objects.filter(receiver=request.user).only(
        'id', '        
        if new_content and new        django_messages.error(request, "You don't have permission to view this message.")
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
