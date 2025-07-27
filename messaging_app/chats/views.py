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

class MessageViewSet(ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsParticipantOfConversation]
    pagination_class = CustomMessagePagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = MessageFilter
    ordering_fields = ["sent_at"]
    ordering = ["-sent_at"]

    def get_queryset(self):
        return Message.objects.filter(conversation__participants__user=self.request.user).distinct()

    def perform_create(self, serializer):
        conversation = serializer.validated_data.get("conversation")

        if not conversation.participants.filter(user=self.request.user).exists():
            return Response(
                {"detail": "You are not a participant of this conversation."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer.save(sender=self.request.user)

class ConversationViewSet(ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [IsParticipantOfConversation]

    def get_queryset(self):
        return Conversation.objects.filter(participants__user=self.request.user).distinct()
