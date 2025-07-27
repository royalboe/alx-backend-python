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

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()
    permission_classes = [IsAuthenticated, IsOwner, IsParticipantOfConversation]
    pagination_class = CustomMessagePagination

    def perform_create(self, serializer):
        # Explicitly get conversation_id from validated data
        conversation_id = serializer.validated_data.get("conversation").id
        conversation = serializer.validated_data.get("conversation")

        if not conversation.participants.filter(user_id=self.request.user.user_id).exists():
            raise PermissionDenied(detail="You are not a participant in this conversation.")

        serializer.save(sender=self.request.user)
class ConversationViewSet(ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [IsParticipantOfConversation]

    def get_queryset(self):
        return Conversation.objects.filter(participants__user=self.request.user).distinct()
