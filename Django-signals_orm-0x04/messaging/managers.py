from django.db.models import Manager

class UnreadMessagesManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(read=False)
    
    def for_user(self, user):
        """
        Get unread messages for user
        """
        return self.get_queryset().filter(receiver=user).only(
            'id', 'sender', 'content', 'timestamp'
        ).select_related('sender')