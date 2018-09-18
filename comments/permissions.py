from rest_framework import permissions


class CanSeeComment(permissions.BasePermission):
    """
        Object-level permission for comments, checks if user can see comments.
    """

    def has_object_permission(self, request, view, obj):
        can_see = True
        if request.user in obj.post.community.banned_users.all():
            can_see = False
        elif obj.post.community.invitation_required:
            if request.user not in obj.post.community.invited_users.all():
                can_see = False
        return can_see


class IsOwner(permissions.BasePermission):
    """
        Object-level permission for comments, checks if user is owner.
    """

    def has_object_permission(self, request, view, obj):
        return request.user == obj.posted_by
