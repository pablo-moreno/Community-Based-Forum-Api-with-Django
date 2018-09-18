from rest_framework import generics, permissions as rest_permissions
from . import serializers, models, pagination, permissions


class CreateCommunity(generics.CreateAPIView):
    """
        Create a community, user has to be logged in to create it.
    """

    serializer_class = serializers.CreateCommunitySerializer
    permission_classes = (rest_permissions.IsAuthenticated, )

    def perform_create(self, serializer):
        serializer.save(administrator=self.request.user)


class DestroyCommunity(generics.UpdateAPIView):
    """
        Destroys community by setting communitys is_active to false.
    """

    serializer_class = serializers.DestroyCommunitySerializer
    permission_classes = (permissions.IsCommunityAdmin, )
    queryset = models.Community.objects.all()
    lookup_field = 'slug'


class UpdateCommunity(generics.UpdateAPIView):
    """
        Updates community settings, needs to be community administrator.
    """

    serializer_class = serializers.UpdateCommunitySerializer
    permission_classes = (permissions.IsCommunityAdmin,)
    queryset = models.Community.objects.all()
    lookup_field = 'slug'


class ModeratorUpdateCommunity(generics.UpdateAPIView):
    """
        Updates banned_users and invited_users of a community, needs to be community moderator.
    """

    serializer_class = serializers.ModeratorUpdateCommunitySerializer
    permission_classes = (permissions.IsCommunityModerator,)
    queryset = models.Community.objects.all()
    lookup_field = 'slug'


class RetrieveCommunity(generics.RetrieveAPIView):
    """
        Retrieves community.
    """

    serializer_class = serializers.RetrieveCommunitySerializer
    queryset = models.Community.objects.filter(is_active=True)
    permission_classes = (permissions.CanSeeCommunity, )
    lookup_field = 'slug'

    def get_serializer_context(self):
        context = super(RetrieveCommunity, self).get_serializer_context()
        context.update({'user': self.request.user})
        return context


class RetrieveCommunitiesAdministratedByUser(generics.ListAPIView):
    """
        Retrieves communities administrated by user.
    """

    serializer_class = serializers.RetrieveCommunitiesAdministratedByUser
    permission_classes = (rest_permissions.IsAuthenticated, )
    pagination_class = pagination.CommunityPagination

    def get_queryset(self):
        return models.Community.objects.filter(administrator=self.request.user)


class RetrieveCommunitiesModeratedByUser(generics.ListAPIView):
    """
        Retrieves communities moderated by user.
    """

    serializer_class = serializers.RetrieveCommunitiesModeratedByUser
    permission_classes = (rest_permissions.IsAuthenticated, )
    pagination_class = pagination.CommunityPagination

    def get_queryset(self):
        return models.Community.objects.filter(moderators=self.request.user)
