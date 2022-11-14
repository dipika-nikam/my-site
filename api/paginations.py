from rest_framework import pagination

class CustomPagePagination(pagination.PageNumberPagination):
    page_size=15
    page_query_param='page'
    max_page_size=15
    page_size_query_param='page'
