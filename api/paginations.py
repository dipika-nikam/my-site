from rest_framework import pagination

class CustomPagePagination(pagination.PageNumberPagination):
    page_size=5
    page_query_param='page'
    max_page_size=5
    page_size_query_param='page'

class AppointmentPagePagination(pagination.PageNumberPagination):
    page_size=5
    page_query_param='page'
    max_page_size=5
    page_size_query_param='page'
