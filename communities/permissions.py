from rest_framework import permissions


class IsCommunityAdmin(permissions.BasePermission):
    """
        Object-level permission for community, checks if user is administrator of the community
    """

    def has_object_permission(self, request, view, obj):
        return obj.is_administrator(request.user)


class IsCommunityModerator(permissions.BasePermission):
    """
        Object-level permission for community, checks if user is moderator of the community
    """

    def has_object_permission(self, request, view, obj):
        if obj.is_administrator(request.user):
            return True
        return obj.is_moderator(request.user)


class CanSeeCommunity(permissions.BasePermission):
    """
        Object-level permission for community, checks if user can see community
    """

    def has_object_permission(self, request, view, obj):
        can_see = True
        if request.user in obj.banned_users.all():
            can_see = False
        elif obj.invitation_required:
            if request.user not in obj.invited_users.all():
                can_see = False
        return can_see
