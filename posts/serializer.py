from rest_framework import serializers
from . import models


class RetrievePostListSerializer(serializers.ModelSerializer):
    """
        Serializer for post list.
    """

    title = serializers.SerializerMethodField()
    post_link = serializers.HyperlinkedIdentityField(view_name='retrieve-post', lookup_field='slug')

    def get_title(self, object):
        return object.title if object.is_active else "deleted"

    class Meta:
        model = models.Post
        fields = ('title', 'votes', 'posted_by', 'comments_count', 'post_link')


class RetrievePostSerializer(serializers.ModelSerializer):
    """
        Serializer for individual post.
    """
    description = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    def get_description(self, object):
        return object.description if object.is_active else "deleted"

    def get_title(self, object):
        return object.title if object.is_active else "deleted"

    def get_url(self, object):
        return object.url if object.is_active else "deleted"

    class Meta:
        model = models.Post
        fields = ('title', 'description', 'votes', 'locked', 'posted_by', 'url', 'comments_count')


class UpdatePostSerializer(serializers.ModelSerializer):
    """
        Serializer for updating a post.
    """

    class Meta:
        model = models.Post
        fields = ('title', 'description', 'votes', 'locked', 'url')


class CreatePostSerializer(serializers.ModelSerializer):
    """
        Serializer for creating a post.
    """

    class Meta:
        model = models.Post
        fields = ('title', 'description', 'url')


class DeletePostSerializer(serializers.ModelSerializer):
    """
        Serializer for post deactivation.
    """

    class Meta:
        model = models.Post
        fields = ('is_active', )
