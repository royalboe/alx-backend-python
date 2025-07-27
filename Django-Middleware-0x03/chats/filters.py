import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    """
    Filter messages by sender, recipient, or creation time range.
    """
    created_at__gte = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_at__lte = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    sender = django_filters.NumberFilter(field_name='sender__id')
    conversation = django_filters.NumberFilter(field_name='conversation__id')

    class Meta:
        model = Message
        fields = ['sender', 'conversation', 'created_at__gte', 'created_at__lte']
