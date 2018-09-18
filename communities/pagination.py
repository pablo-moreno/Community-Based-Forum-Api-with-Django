from rest_framework import pagination


class CommunityPagination(pagination.PageNumberPagination):
    page_size = 20
