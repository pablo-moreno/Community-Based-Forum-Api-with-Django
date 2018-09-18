from rest_framework import generics, filters, exceptions, permissions as rest_permissions
from . import serializer, models, pagination, permissions
from communities import models as community_models


class RetrievePostList(generics.ListAPIView):
    """
        Retrieve a list of posts from a community.
    """

    serializer_class = serializer.RetrievePostListSerializer
    pagination_class = pagination.PostsPagination
    filter_backends = (filters.OrderingFilter, filters.SearchFilter)
    search_fields = ('title', 'description')

    def get_queryset(self):
        community = community_models.Community.objects.get(slug=self.kwargs.get('community'))
        if not community.is_active:
            raise exceptions.NotFound()
        return models.Post.objects.filter(community=community)


class RetrievePost(generics.RetrieveAPIView):
    """
        Retrieve individual posts.
    """

    serializer_class = serializer.RetrievePostSerializer
    queryset = models.Post.objects.all()
    permission_classes = (permissions.CanSeePost, )
    lookup_field = 'slug'


class UpdatePost(generics.UpdateAPIView):
    """
        Updates a post.
    """

    serializer_class = serializer.UpdatePostSerializer
    queryset = models.Post.objects.filter(is_active=True)
    permission_classes = (permissions.IsOwner, )
    lookup_field = 'slug'


class CreatePost(generics.CreateAPIView):
    """
        Creates a post.
    """

    serializer_class = serializer.CreatePostSerializer
    permission_classes = (rest_permissions.IsAuthenticated, )

    def perform_create(self, serializer):
        community = community_models.Community.objects.get(slug=self.kwargs.get('community'))
        serializer.save(posted_by=self.request.user, community=community)


class DeletePost(generics.UpdateAPIView):
    """
        Deactivates a post.
    """

    serializer_class = serializer.DeletePostSerializer
    queryset = models.Post.objects.filter(is_active=True)
    permission_classes = (permissions.IsOwner, )
    lookup_field = 'slug'
