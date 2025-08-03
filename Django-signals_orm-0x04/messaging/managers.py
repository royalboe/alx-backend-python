from django.db.models import Manager

class UnreadMessagesManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(read=False)
    
    def unread_for_user(self, user):
        """
        Get unread messages for user
        """
        return self.get_queryset().filter(receiver=user).select_related('sender')