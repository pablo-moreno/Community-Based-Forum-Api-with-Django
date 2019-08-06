from rest_framework import serializers, exceptions
from . import models


class CreateCommunitySerializer(serializers.ModelSerializer):
    """
        Serializer for community creation.
    """

    url = serializers.HyperlinkedIdentityField(view_name='retrieve-community', lookup_field='slug', read_only=True)

    class Meta:
        model = models.Community
        fields = ('name', 'url')


class UpdateRetrieveDestroyCommunitySerializer(serializers.ModelSerializer):
    """
        Serializer for updating community as admin.
    """

    is_active = serializers.BooleanField(read_only=True)

    @staticmethod
    def check_and_return_color(color):
        if color:
            text_color = len(str(abs(color)))
            if text_color != 6:
                raise exceptions.ValidationError('Text color must have 6 characters')
        return color

    @staticmethod
    def validate_text_color(color):
        return UpdateRetrieveDestroyCommunitySerializer.check_and_return_color(color)

    @staticmethod
    def validate_background_color(color):
        return UpdateRetrieveDestroyCommunitySerializer.check_and_return_color(color)

    class Meta:
        model = models.Community
        fields = ('invitation_required', 'adult', 'text_color', 'background_color', 'background_img',
                  'banned_users', 'invited_users', 'moderators', 'is_active')
