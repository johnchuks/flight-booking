from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    object level permission to only allow owners view  and edit the content.
    """

    def has_object_permission(self, request, view, obj):
        if obj.user == request.user:
            return True
        else:
            return False
