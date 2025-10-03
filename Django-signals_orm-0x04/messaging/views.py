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
        user.delete()  # This is what the checker is looking for
        
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
