from rest_framework.pagination import PageNumberPagination

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
