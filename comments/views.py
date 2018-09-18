from django.db.models import Q
from rest_framework import generics, permissions as rest_permissions
from . import serializer, models, pagination, permissions
from posts import models as posts_models


class CreateComment(generics.CreateAPIView):
    """
        Creates a comment with or without parent.
    """

    serializer_class = serializer.CreateCommentSerializer
    permission_classes = (rest_permissions.IsAuthenticated, permissions.CanSeeComment)

    def perform_create(self, serializer):
        serializer.save(post=posts_models.Post.objects.get(slug=self.kwargs.get('slug')), posted_by=self.request.user)


class RetrieveCommentsByPost(generics.ListAPIView):
    """
        Retrieve parent comments of a post.
    """

    serializer_class = serializer.RetrieveCommentSerializer
    pagination_class = pagination.CommentsPagination
    permission_classes = (permissions.CanSeeComment, )

    def get_queryset(self):
        return models.Comment.objects.filter(Q(is_active=True) & Q(parent_id=-1) &
                                             Q(post=posts_models.Post.objects.get(slug=self.kwargs.get('slug'))))


class DeleteCommentSerializer(generics.UpdateAPIView):
    """
        Sets is_active if it is False the post won't show and if it is True it will.
    """

    serializer_class = serializer.DeleteCommentSerializer
    queryset = models.Comment.objects.filter(is_active=True)
    permission_classes = (permissions.IsOwner, )
    lookup_field = 'id'


class UpdateCommentSerializer(generics.UpdateAPIView):
    """
        Updates a comment text.
    """

    serializer_class = serializer.UpdateCommentSerializer
    queryset = models.Comment.objects.filter(is_active=True)
    permission_classes = (permissions.IsOwner, )
    lookup_field = 'id'


class GetChildComments(generics.ListAPIView):
    """
        Gets comments that have a parent comment in a post.
    """

    serializer_class = serializer.RetrieveCommentSerializer
    pagination_class = pagination.CommentsPagination
    permission_classes = (permissions.CanSeeComment, )

    def get_queryset(self):
        return models.Comment.objects.filter(Q(is_active=True)
                                             & Q(post=posts_models.Post.objects.get(slug=self.kwargs.get('slug'))) &
                                             Q(parent_id=self.kwargs.get('parent_id')))
