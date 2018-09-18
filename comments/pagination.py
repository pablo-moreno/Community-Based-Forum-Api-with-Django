from rest_framework import pagination


class CommentsPagination(pagination.PageNumberPagination):
    page_size = 60
