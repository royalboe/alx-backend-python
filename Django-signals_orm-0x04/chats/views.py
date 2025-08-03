from rest_framework import viewsets, status
from rest_framework.response import Response
from messaging.models import User, Message, Notification, MessageHistory
from messaging.serializers import UserSerializer, MessageHistorySerializer, MessageSerializer, NotificationSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.views.decorators.cache import cache_page


class MessageView(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Optimized query to get messages sent by the user with replies preloaded.
        Get all the root conversations first and prefetch the replies
        """
        request = self.request
        return (
            Message.objects.filter(sender=request.user, parent_message__isnull=True)
            .select_related('sender', 'receiver')
            .prefetch_related('replies__sender'))
    
    @cache_page(60)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @action(detail=True, methods=['get'])
    def thread(self, request, pk=None):
        """
        Recursively fetch all replies to a message (threaded view).
        """
        message = self.get_object()

        def get_replies(msg):
            replies = []
            for reply in msg.replies.all():
                reply_data = MessageSerializer(reply).data
                reply_data['replies'] = get_replies(reply)
                replies.append(reply_data)
            return replies

        root_data = MessageSerializer(message).data
        root_data['replies'] = get_replies(message)
        return Response(root_data)
    
    @action(detail=False, methods=['get'])
    def unread(self, request, pk=None):
        """
        Fetch all unread messages sent to the user.
        """
        unread_messages = Message.unread.unread_for_user(user=request.user).only(
            'id', 'sender', 'content', 'timestamp'
        )
        serializer = self.get_serializer(unread_messages, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        """
        Mark message as read
        """
        message = self.get_object()
        if message.receiver != request.user:
            return Response({"detail": "Not allowed."}, status=403)

        message.read = True
        message.save()
        return Response({"detail": "Marked as read."}, status=status.HTTP_202_ACCEPTED)
    
