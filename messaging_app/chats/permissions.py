from rest_framework import permissions
from .models import Conversation, Message

class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow the sender of a message to access it.
    """
    def has_object_permission(self, request, view, obj):
        return request.user == obj.sender
    

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to ensure that only participants of a conversation 
    are granted access to view or interact with it.
    """
    def has_object_permission(self, request, view, obj):
         """
        Check if the requesting user is one of the participants in the conversation.

        Args:
            request: The HTTP request object.
            view: The view being accessed.
            obj: The conversation instance being checked.

        Returns:
            bool: True if the user is a participant, False otherwise.
        """

         return obj.participants.filter(user_id=request.user.user_id).exists()
    
    def has_permission(self, request, view):
        """
        Ensure the user is authenticated before allowing access.

        Args:
            request: The HTTP request object.
            view: The view being accessed.

        Returns:
            bool: True if the user is authenticated, False otherwise.
        """
        return request.user and request.user.is_authenticated