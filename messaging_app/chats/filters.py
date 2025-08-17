"""
REQUIREMENTS:
Using django-filters , 
Add filtering class MessageFilter to your views 
to retrieve conversations with specific users or 
messages within a time range
"""
from django_filters import rest_framework as filters

from .models import Message
from django.utils import timezone
from datetime import timedelta
from django.conf import settings

class MessageFilter(filters.FilterSet):
    
    class Meta:
        model = Message
        fields = {
            'conversation__participants__user_id': ['exact'],
            'sender__user_id': ['exact'],
            'conversation__conversation_id': ['exact'],
            'sent_at': ['gte', 'lte', 'exact', 'gt', 'lt']
        }

class MessageFilter(filters.FilterSet):
    """
    Filter messages by:
    - participant in the conversation
    - sender
    - conversation
    - sent date range
    """
    # Time range filters
    sent_after = filters.DateTimeFilter(field_name='sent_at', lookup_expr='gte')
    sent_before = filters.DateTimeFilter(field_name='sent_at', lookup_expr='lte')
    
    # Direct sender filter
    sender = filters.UUIDFilter(field_name='sender__user_id')

    # Conversation filter
    conversation = filters.UUIDFilter(field_name='conversation__conversation_id')

    # Participant filter
    participant = filters.UUIDFilter(field_name='conversation__participants__user_id')

    class Meta:
        model = Message
        fields = ['sender', 'conversation', 'participant', 'sent_after', 'sent_before']

    @property
    def qs(self):
        """
        Override qs to apply a default date filter if no date filters are provided.
        Reads the default days from settings.MESSAGE_DEFAULT_DAYS.
        """
        queryset = super().qs
        if not self.data.get('sent_after') and not self.data.get('sent_before'):
            default_days = getattr(settings, 'MESSAGE_DEFAULT_DAYS', 7)
            cutoff_date = timezone.now() - timedelta(days=default_days)
            queryset = queryset.filter(sent_at__gte=cutoff_date)
        return queryset