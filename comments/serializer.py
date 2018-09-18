from rest_framework import serializers

from . import models as comment_models


class CreateCommentSerializer(serializers.ModelSerializer):
    """
        Serializer for comments creation.
    """

    class Meta:
        model = comment_models.Comment
        fields = ('sticky', 'comment', 'parent_id')


class RetrieveCommentSerializer(serializers.ModelSerializer):
    """
        Serializer for retrieving comments.
    """

    class Meta:
        model = comment_models.Comment
        fields = ('posted_by', 'sticky', 'comment', 'creation_date', 'votes')


class DeleteCommentSerializer(serializers.ModelSerializer):
    """
        Serializer for "deactivating"/"activating" comments.
    """

    class Meta:
        model = comment_models.Comment
        fields = ('is_active', )


class UpdateCommentSerializer(serializers.ModelSerializer):
    """
        Serializer for updating comments.
    """

    class Meta:
        model = comment_models.Comment
        fields = ('comment', )
