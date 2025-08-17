from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated, 
    IsAdminUser, 
    IsAuthenticatedOrReadOnly,
    AllowAny
    )
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from django_filters import rest_framework as filters
from rest_framework import filters as filter


from .permissions import IsParticipantOfConversation
from .models import User, Message, Conversation
from .serializers import UserSerializer, MessageSerializer, ConversationSerializer
from .filters import MessageFilter
from .pagination import CustomMessagePagination

class HealthCheckView(APIView):
    def get(self, request):
        return Response({"status": "OK"})


class ExampleView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    print("INSIDE EXAMPLEVIEW GET")


    def get(self, request, format=None):
        return Response({
            'user_id': request.user.user_id,
            'email': request.user.email,
            'auth': str(request.auth),
        })


# class ExampleView(viewsets.ModelViewSet):
#     authentication_classes = [JWTAuthentication, SessionAuthentication, BasicAuthentication]
#     permission_classes = [IsAuthenticated]
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     lookup_field = 'user_id'

#     def list(self, request, *args, **kwargs):
#         content = {
#             'user': str(request.user),
#             'auth': str(request.auth),
#         }
#         return Response(content)
    

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [
        filters.DjangoFilterBackend,
        filter.SearchFilter,
        filter.OrderingFilter
        ]
    search_fields = ['first_name', 'last_name', 'email']
    # search_fields = ['=first_name', '=last_name', '=email'] exact matches
    ordering_fields = ['last_seen']
    ordering = ['first_name']
    # permission_classes = [IsAuthenticated, IsAdminUser]


    def get_permissions(self):
        """ Set permissions based on action"""

        # Allows anyone to create an account
        # but restricts other actions to authenticated users
        # and admin users for update/delete actions.
        if self.action == 'create':
            self.permission_classes = [AllowAny]
        elif self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated, IsAdminUser]
        elif self.action in ['list', 'retrieve']:
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.prefetch_related(
        'sender',
        'conversation'
    ).all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filterset_class = MessageFilter
    pagination_class = CustomMessagePagination

    def get_queryset(self):
        """
        To get messages that the user can read
        """
        qs = super().get_queryset()
        return qs.filter(conversation__participants__user_id=self.request.user.user_id)

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.prefetch_related(
        'messages', 
        'participant_links', 
        'participants', 
        'messages__sender',
        'messages__conversation'
        ).all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        """
        To get only conversations that the user is a participant of
        """
        qs = super().get_queryset()
        print(self.request.user.user_id)
        # return super().get_queryset()
        return qs.filter(participants__user_id=self.request.user.user_id)
