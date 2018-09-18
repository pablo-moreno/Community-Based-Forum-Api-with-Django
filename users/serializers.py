from rest_framework import serializers
from users import models


class UserSerializer(serializers.ModelSerializer):
    """
        Serializer for user model.
    """

    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    def validate_password(self, data):
        if len(data) < 6:
            raise serializers.ValidationError("Password length less than 6 characters")
        return data

    class Meta:
        model = models.User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}



