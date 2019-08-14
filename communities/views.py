from rest_framework import generics, permissions as rest_permissions
from . import serializers, models, pagination, permissions


class ListCreateCommunity(generics.ListCreateAPIView):
    serializer_class = serializers.CreateCommunitySerializer
    permission_classes = (rest_permissions.IsAuthenticated, )
    queryset = models.Community.objects.all()
    pagination_class = pagination.CommunityPagination

    def perform_create(self, serializer):
        serializer.save(administrator=self.request.user)

    def get_queryset(self):
        user_type = self.request.query_params.get('user_type')
        if user_type == 'moderators':
            return self.queryset.filter(moderators=self.request.user)
        else:
            return self.queryset


class UpdateRetrieveDestroyCommunityAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.UpdateRetrieveDestroyCommunitySerializer
    permission_classes = (permissions.IsCommunityAdmin, permissions.IsCommunityModerator)
    queryset = models.Community.objects.all()
    lookup_field = 'id'
