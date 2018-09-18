from rest_framework import pagination


class PostsPagination(pagination.PageNumberPagination):
    page_size = 20
