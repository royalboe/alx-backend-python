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
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        """
        Customize the paginated response to include total count and pagination details.
        """
        return Response({
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
        })
