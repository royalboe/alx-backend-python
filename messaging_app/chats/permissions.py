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
        Allow access only if the user is a participant in the conversation.
        For PUT/PATCH/DELETE on messages, the user must also be the sender.
        """

        user_id = request.user.user_id

        # Case: object is a Conversation
        if hasattr(obj, 'participants'):
            return obj.participants.filter(user_id=user_id).exists()

        # Case: object is a Message
        if hasattr(obj, 'conversation'):
            is_participant = obj.conversation.participants.filter(user_id=user_id).exists()

            if request.method in ("PUT", "PATCH", "DELETE"):
                return is_participant and obj.sender_id == user_id

            return is_participant

        # Deny all by default
        return False

    
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
    