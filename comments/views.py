from django.db.models import Q
from rest_framework import generics, permissions as rest_permissions
from . import serializer, models, pagination, permissions
from posts import models as posts_models


class ListCreateCommentAPIView(generics.ListCreateAPIView):
    serializer_class = serializer.RetrieveCommentSerializer
    permission_classes = (rest_permissions.IsAuthenticated, permissions.CanSeeComment)

    def perform_create(self, serializer):
        serializer.save(post=posts_models.Post.objects.get(id=self.kwargs.get('id')), posted_by=self.request.user)

    def get_queryset(self):
        return models.Comment.objects.filter(is_active=True, post__id=self.kwargs.get('id'))


class RetrieveUpdateDestroyCommentAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializer.RetrieveCommentSerializer
    queryset = models.Comment.objects.filter(is_active=True)
    permission_classes = (permissions.IsOwner, )
    lookup_field = 'id'


class GetChildCommentsAPIView(generics.ListAPIView):
    serializer_class = serializer.RetrieveCommentSerializer
    pagination_class = pagination.CommentsPagination
    permission_classes = (permissions.CanSeeComment, )

    def get_queryset(self):
        return models.Comment.objects.filter(Q(is_active=True)
                                             & Q(post=posts_models.Post.objects.get(id=self.kwargs.get('id'))) &
                                             Q(parent_id=self.kwargs.get('parent_id')))
