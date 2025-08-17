from rest_framework.permissions import BasePermission
from .models import Message, Conversation

class IsParticipantOfConversation(BasePermission):
    
    def is_participant(self, user, conversation):
        """
        Check if the user is a participant of the conversation.

        Args:
            user: The user object.
            conversation: The conversation object.

        Returns:
            bool: True if the user is a participant, False otherwise.
        """
        return conversation.participants.filter(user_id=user.user_id).exists()

    """
    Custom permission: only allow owners of an object to access it.
    """
    def has_permission(self, request, view):
        """
          Allow access only if the user is a participant in the conversation.
          Args:
              request: The HTTP request object.
              view: The view being accessed.

          Returns:
              bool: True if the user is authenticated, False otherwise.
        """
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        """
        Ensure that the user is a part of
        Args:
            request: The HTTP request object.
            view: The view being accessed.
            obj: The object being accessed.

        Returns:
            bool: True if the user is a participant of the conversation, False otherwise.
        """
        user = request.user

        if isinstance(obj, Conversation):
            # For conversations, check if the user is a participant
            return self.is_participant(user, obj)

        if isinstance(obj, Message):
            # For messages, check if the user is the sender
            if request.method.upper() in ['PUT', 'PATCH', 'DELETE']:
                # For PUT/PATCH/DELETE, check if the user is the sender
                if user.conversation_id != obj.conversation_id:
                    return False
                return self.is_participant(user, obj.conversation) and obj.sender == user
            return self.is_participant(user, obj.conversation)
        
        return False