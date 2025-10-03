from django.db import models

class UnreadMessagesManager(models.Manager):
    """
    Task 4: Custom manager for unread messages
    """
    def get_queryset(self):
        return super().get_queryset().filter(read=False)
    
    def unread_for_user(self, user):
        """
        Task 4: Filter unread messages for a specific user with .only() optimization
        """
        return self.get_queryset().filter(receiver=user).only(
            'id', 'content', 'sender__username', 'timestamp', 'read'
        )

class MessageManager(models.Manager):
    """
    Enhanced manager for Message model with optimized queries
    """
    def get_queryset(self):
        return super().get_queryset().select_related('sender', 'receiver')
    
    def threaded_conversations(self):
        """
        Task 3: Get messages with optimized replies prefetching
        """
        return self.get_queryset().prefetch_related(
            'replies__sender',
            'replies__re
