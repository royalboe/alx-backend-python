from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import User, Message, Notification, MessageHistory
from .serializers import UserSerializer, MessageHistorySerializer, MessageSerializer, NotificationSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
# Create your views here.
class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # def destroy(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     self.perform_destroy(instance)
    #     return Response(status=status.HTTP_204_NO_CONTENT)
    @action(detail=False, methods=['delete'], permission_classes=[IsAuthenticated])
    def delete_user(self, request):
        """
        Custom endpoint for a user to delete their own account.
        """
        request.user.delete()
        return Response({"detail": "Your account has been deleted."}, status=status.HTTP_204_NO_CONTENT)

class MessageView(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Use prefetchrelated and selectrelated to optimize querying of messages and their replies, reducing the number of database queries.
        """
        qs = super().get_queryset()
        qs = qs.select_related('sender=request.user', 'receiver')
        qs = qs.prefetch_related('replies')
        return qs