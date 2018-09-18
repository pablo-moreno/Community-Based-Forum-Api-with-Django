from rest_framework import permissions
from communities import models as community_models


class IsOwner(permissions.BasePermission):
    """
        Object-level permission for posts, checks if is owner of post.
    """

    def has_object_permission(self, request, view, obj):
        return obj.posted_by == request.user


class CanSeePost(permissions.BasePermission):
    """
        Checks if user can see post.
    """

    def has_object_permission(self, request, view, obj):
        can_see = True
        if request.user in obj.community.banned_users.all():
            can_see = False
        elif obj.community.invitation_required:
            if request.user not in obj.community.invited_users.all():
                can_see = False
        return can_see
