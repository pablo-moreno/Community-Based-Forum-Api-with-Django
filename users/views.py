from rest_framework import generics, permissions
from . import models, serializers


class UserProfile(generics.RetrieveAPIView):
    """
        Get user profile.
    """

    serializer_class = serializers.UserSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_object(self):
        return models.User.objects.get(pk=self.request.user.pk)


class CreateUser(generics.CreateAPIView):
    """
        Create an user.
    """

    serializer_class = serializers.UserSerializer

    def perform_create(self, serializer):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        serializer.save(ip=ip)


