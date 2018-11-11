from rest_framework import permissions



class IsOwnerOrAdmin(permissions.BasePermission):
    """
    object level permission to only allow only owners or admin view the content.
    """

    def has_object_permission(self, request, view, obj):
        if obj.user == request.user or request.user.is_staff:
            return True
        else:
            return False
