from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation to access it.
    """
    
    def has_object_permission(self, request, view, obj):
        # Check if the user is a participant in the conversation
        if hasattr(obj, 'participants'):
            # For Conversation objects
            return request.user in obj.participants.all()
        elif hasattr(obj, 'conversation'):
            # For Message objects
            return request.user in obj.conversation.participants.all()
        return False
    
    def has_permission(self, request, view):
        # Allow only authenticated users
        return request.user and request.user.is_authenticated
