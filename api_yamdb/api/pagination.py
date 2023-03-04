from rest_framework import pagination


class CustomPagination(pagination.PageNumberPagination):
    """Пагинация в виде списка."""

    page_size = 4
    page_size_query_param = "page_size"
    max_page_size = 10000
