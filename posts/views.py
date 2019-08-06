from rest_framework import generics, filters, exceptions
from . import serializer, models, pagination, permissions
from communities import models as community_models


class ListCreatePostsAPIView(generics.ListCreateAPIView):
    serializer_class = serializer.RetrieveUpdateDestroyPostSerializer
    pagination_class = pagination.PostsPagination
    filter_backends = (filters.OrderingFilter, filters.SearchFilter)
    search_fields = ('title', 'description')

    def get_queryset(self):
        community = community_models.Community.objects.get(slug=self.kwargs.get('community'))
        if not community.is_active:
            raise exceptions.NotFound()
        return models.Post.objects.filter(community=community)

    def perform_create(self, serializer_local):
        community = community_models.Community.objects.get(slug=self.kwargs.get('community'))
        serializer_local.save(posted_by=self.request.user, community=community)


class RetrieveUpdateDestroyPostAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializer.ListCreatePostSerializer
    queryset = models.Post.objects.all()
    permission_classes = (permissions.IsOwner, )
    lookup_field = 'id'

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = (permissions.CanSeePost, )
        return super().get_permissions()
