from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomMessagePagination(PageNumberPagination):
    """
    Custom pagination class for paginating messages in a consistent and controlled way.

    Attributes:
        page_size (int): Default number of items per page.
        page_size_query_param (str): Query parameter to override the default page size.
        max_page_size (int): Maximum allowed page size that can be requested.
    """
    page_size = 20
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        """
        Customize the paginated response to include total count and pagination details.
        """
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
                },
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'page_size': self.get_page_size(self.request),
            'max_page_size': self.max_page_size,
            'has_next': self.page.has_next(),
            'has_previous': self.page.has_previous(),
            'results': data,
        })