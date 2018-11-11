from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    object level permission to only allow only owners or admin view the content.
    """

    def has_object_permission(self, request, view, obj):
        if obj.user == request.user:
            return True
        else:
            return False
