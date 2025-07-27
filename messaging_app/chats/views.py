from .models import User, Message, Conversation
from .serializers import UserSerializer, MessageSerializer, ConversationSerializer
from .permissions import IsOwner, IsParticipantOfConversation
from .pagination import CustomMessagePagination
from .filters import MessageFilter

from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from .models import Message, Conversation
from .serializers import MessageSerializer
from .permissions import IsParticipantOfConversation

from rest_framework.exceptions import PermissionDenied

from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend

from .models import Message, Conversation
from .serializers import MessageSerializer
from .permissions import IsOwner, IsParticipantOfConversation
from .pagination import CustomMessagePagination
from .filters import MessageFilter


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.none()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsOwner, IsParticipantOfConversation]
    pagination_class = CustomMessagePagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = MessageFilter
    ordering_fields = ["sent_at"]
    ordering = ["-sent_at"]

    def get_queryset(self):
        """
        Restrict messages to participants of a specific conversation.
        Ensures conversation_id is passed and valid.
        """
        conversation_id = self.request.query_params.get("conversation_id")
        if not conversation_id:
            raise PermissionDenied(detail="conversation_id is required.")

        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            raise PermissionDenied(detail="Conversation does not exist.")

        if not conversation.participants.filter(user_id=self.request.user.user_id).exists():
            from rest_framework.status import HTTP_403_FORBIDDEN
            raise PermissionDenied(detail="You are not a participant of this conversation.")

        return Message.objects.filter(conversation_id=conversation_id)

class ConversationViewSet(ModelViewSet):
    queryset = Message.objects.none()
    serializer_class = ConversationSerializer
    permission_classes = [IsParticipantOfConversation]

    def get_queryset(self):
        return Conversation.objects.filter(participants__user=self.request.user).distinct()
