from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """
    Custom permission to only allow access to the owner of the object.
    """

    message = 'You do not have permission to perform this action.'
    
    def has_object_permission(self, request, view, obj):
        return request.user == obj


class IsOwnerOrAdmin(BasePermission):
    """
    Custom permission to allow access to the owner of the object or an admin user.
    """

    message = 'You do not have permission to perform this action.'
    
    def has_object_permission(self, request, view, obj):
        return (request.user == obj or request.user.is_superuser)
