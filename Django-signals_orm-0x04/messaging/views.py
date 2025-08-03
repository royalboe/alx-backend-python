from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import User, Message, Notification, MessageHistory
from .serializers import UserSerializer, MessageHistorySerializer, MessageSerializer, NotificationSerializer

# Create your views here.
class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # def destroy(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     self.perform_destroy(instance)
    #     return Response(status=status.HTTP_204_NO_CONTENT)
    
