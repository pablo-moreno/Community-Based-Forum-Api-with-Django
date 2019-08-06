from rest_framework import serializers

from . import models as comment_models


class RetrieveCommentSerializer(serializers.ModelSerializer):
    """
        Serializer for retrieving comments.
    """

    is_active = serializers.BooleanField(write_only=True)
    parent_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = comment_models.Comment
        fields = ('posted_by', 'sticky', 'comment', 'creation_date', 'votes', 'is_active')
