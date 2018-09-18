from rest_framework import serializers, exceptions
from . import models


class CreateCommunitySerializer(serializers.ModelSerializer):
    """
        Serializer for community creation.
    """

    class Meta:
        model = models.Community
        fields = ('name', )


class UpdateCommunitySerializer(serializers.ModelSerializer):
    """
        Serializer for updating community as admin.
    """

    def validate_text_color(self, color):
        if color:
            text_color = len(str(abs(color)))
            if text_color != 6:
                raise exceptions.ValidationError('Text color must have 6 characters')
        return color

    def validate_background_color(self, color):
        if color:
            background_color = len(str(abs(color)))
            if background_color != 6:
                raise exceptions.ValidationError('Text color must have 6 characters')
        return color

    class Meta:
        model = models.Community
        fields = ('invitation_required', 'adult', 'text_color', 'background_color', 'background_img',
                  'banned_users', 'invited_users', 'moderators')


class ModeratorUpdateCommunitySerializer(serializers.ModelSerializer):
    """
        Serializer for updating community as moderator.
    """

    class Meta:
        model = models.Community
        fields = ('invited_users', 'banned_users')


class DestroyCommunitySerializer(serializers.ModelSerializer):
    """
        Serializer for destroying community as administrator.
    """

    class Meta:
        model = models.Community
        fields = ('is_active',)


class RetrieveCommunitySerializer(serializers.ModelSerializer):
    """
        Serializer for retrieving community.
    """

    def validate_background_img(self, object):
        return object.background_img.url

    class Meta:
        model = models.Community
        fields = ('name', 'invitation_required', 'adult', 'text_color', 'background_color', 'background_img')


class RetrieveCommunitiesAdministratedByUser(serializers.ModelSerializer):
    """
        Serializer for retrieving communities administrated by a given user.
    """

    url = serializers.HyperlinkedIdentityField(view_name='retrieve-community', lookup_field='slug')

    class Meta:
        model = models.Community
        fields = ('name', 'url')


class RetrieveCommunitiesModeratedByUser(serializers.ModelSerializer):
    """
        Serializer for retrieving communities owned by a given user.
    """

    url = serializers.HyperlinkedIdentityField(view_name='retrieve-community', lookup_field='slug')

    class Meta:
        model = models.Community
        fields = ('name', 'url')

