from rest_framework import serializers
from . import models


class RetrieveUpdateDestroyPostSerializer(serializers.ModelSerializer):
    """
        Serializer for individual post.
    """
    description = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    is_active = serializers.BooleanField(write_only=True)

    def get_description(self, object):
        return object.description if object.is_active else "deleted"

    def get_title(self, object):
        return object.title if object.is_active else "deleted"

    def get_url(self, object):
        return object.url if object.is_active else "deleted"

    class Meta:
        model = models.Post
        fields = ('title', 'description', 'votes', 'locked', 'posted_by', 'url', 'comments_count', 'is_active')


class ListCreatePostSerializer(serializers.ModelSerializer):
    """
        Serializer for creating a post.
    """

    post_link = serializers.HyperlinkedIdentityField(view_name='retrieve-post', lookup_field='slug', read_only=True)

    class Meta:
        model = models.Post
        fields = ('title', 'description', 'url', 'post_link', 'comments_count', 'posted_by', 'votes')

